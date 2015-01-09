#An standalone API for 4store

import sys
import urllib,urllib2
import traceback
import pdb
import time
import json
import os
import subprocess

PREFIXES = """PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc:   <http://purl.org/dc/elements/1.1/>
PREFIX dct:  <http://purl.org/dc/terms/>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX bio:  <http://purl.org/vocab/bio/0.1/>
PREFIX meta: <http://bioportal.bioontology.org/metadata/def/>
PREFIX graphs: <http://purl.bioontology.org/def/graphs/>
PREFIX omv: <http://omv.ontoware.org/2005/05/ontology#>
PREFIX maps: <http://protege.stanford.edu/ontologies/mappings/mappings.rdfs#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX umls: <http://bioportal.bioontology.org/ontologies/umls/>
"""

API_KEY_ADMIN = "null"

class SPARQL:
    def __init__(self,epr,api_key=None):
        self.epr = epr
        self.api_key = api_key
        self.history = []
    def hist(self):
        import pprint
        pprint.pprint(self.history)
    def desc(self,q):
        self.history.append(q)
        return query(PREFIXES+q,self.epr,f='text/plain',api_key=self.api_key)
    def get_data_epr(self):
        return "/".join(self.epr.split("/")[0:-2])+"/data/"

    def pqs(self,q,soft_limit=-1,rules="NONE"):
        self.history.append(q)
        t0 = time.time()
        res = query(PREFIXES+q,self.epr,f='text/plain',api_key=self.api_key,soft_limit=soft_limit,rules=rules)
        tf = time.time()
        print "elapse %.3f"%(tf-t0)
        return s

    def pq(self,q,soft_limit=-1,rules="NONE"):
        print self.pqs(q,soft_limit=soft_limit,rules=rules)

    def query_as_text(self,q):
        self.history.append(q)
        return query(q,self.epr,f='text/plain',api_key=self.api_key)
    def count(self):
        return int(self.query("select (count(?s) as ?c) where { GRAPH ?g { ?s ?p ?o }}")[0]["c"])
    def query(self,x,soft_limit=-1,parse=True):
        self.history.append(x)
        o=query(PREFIXES+x,self.epr,f='application/json',api_key=self.api_key,soft_limit=soft_limit)
        #o=query(PREFIXES+x,self.epr,f='application/sparql-results+xml',api_key=self.api_key,soft_limit=soft_limit)
        if parse:
            return parse_json_result(o)
        else:
            return o
    def ask(self,a):
        res = query(PREFIXES+a,self.epr,f='application/json',api_key=self.api_key)
        return json.loads(res)['boolean']
    def count_in_graph(self,g):
        return int(self.query("select (count(?s) as ?c) where { GRAPH <%s> { ?s ?p ?o }}"%g)[0]["c"])
    def predicates_in_graph(self,g):
        return [x["p"] for x in self.query("select DISTINCT ?p where { GRAPH <%s> { ?s ?p ?o }}"%g)]
    def subjects_in_graph(self,g):
        return [x["s"] for x in self.query("select DISTINCT ?s where { GRAPH <%s> { ?s ?p ?o }}"%g)]
    def objects_in_graph(self,g):
        return [x["o"] for x in self.query("select DISTINCT ?o where { GRAPH <%s> { ?s ?p ?o }}"%g)]
    def types_in_graph(self,g):
        return [x["o"] for x in self.query("select DISTINCT ?o where { GRAPH <%s> { ?s a ?o }}"%g)]
    def get_stats_for_graph(self,g):
        return dict(count=self.count_in_graph(g),
        preds=len(self.predicates_in_graph(g)),
        subs=len(self.subjects_in_graph(g)),
        objs=len(self.objects_in_graph(g)),
        types=len(self.types_in_graph(g)))

    def assert_data_in_graph(self,graph_uri,data,content_format,flushGraph=False):
        return assert_data_in_graph(graph_uri,data,self.get_data_epr(),content_format,flushGraph=flushGraph,queryEpr=self.epr)

    def assert_file_in_graph(self,graph_uri,fpath,content_format,flushGraph=False):
        ret = assert_file_in_graph(graph_uri,fpath,self.get_data_epr(),content_format,flushGraph=flushGraph,queryEpr=self.epr)
        return ret

    def delete_graph(self,graph):
        delete_graph(graph,self.get_data_epr())

    def update(self,u):
        update_epr = "/".join(self.epr.split("/")[:-2]) + "/update/"
        return update4s(u,update_epr,api_key=self.api_key)

    def ping(self):
        query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
        self.pq(query)

    def graphs(self):
        query = "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } } LIMIT 100"
        self.pq(query)


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result

    return timed

def sol2dict(sol):
    d=dict()
    for v in sol:
        if "value" in sol[v]:
            d[v]=sol[v]["value"]
        else:
            d[v]=None

    return d

def parse_json_result(res):
    j=json.loads(res)
    sols = []
    for sol in j["results"]["bindings"]:
        sols.append(sol2dict(sol))
    return sols

def query(q,epr,f='application/json',api_key=None,soft_limit=-1,rules="NONE"):
    try:
        params = {'query': q}
        if api_key:
            print "submitting apikey with query", api_key
            params["apikey"]=api_key
        else:
            pass
            #params["apikey"]=API_KEY_ADMIN
        params["soft-limit"]=str(soft_limit)
        params["rules"]=rules
        params = urllib.urlencode(params)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        #print "request: " + epr+'?'+params
        request = urllib2.Request(epr+'?'+params)
        request.add_header('Accept', f)
        request.get_method = lambda: 'GET'
        url = opener.open(request)
        content = url.read()
        url.close()
        opener.close()
        return content
    except Exception, e:
        traceback.print_exc(file=sys.stdout)
        raise e

def delete_graph(graph,epr):
    delete_with_curl = ["curl","-s","-X","DELETE","%s%s"%(epr,graph)]
    p=subprocess.Popen(delete_with_curl,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    std, err = p.communicate()
    ret = p.poll()
    return ret

def assert_file_in_graph(graph_uri,file_path,
                         epr,content_format,
                         flushGraph=False,queryEpr=None,api_key=None):
   if flushGraph:
       ret = delete_graph(graph_uri,epr)
       if ret <> 0:
          raise Exception, "Unable to delete %s, error message [%s]"%(graph_uri,err)

       if queryEpr:
            sq=SPARQL(queryEpr)
            if sq.count_in_graph(graph_uri) <> 0:
                raise Exception, "Count after delete > 0 (%s)"%graph_uri
   command = None
   if flushGraph:
       command = ["curl","-s",
                  "-T",file_path,
                  "-H","Content-Type: %s"%content_format,
                  "%s%s"%(epr,graph_uri)]
   else:
       command = [ "curl",
            "-s",
            "--data-urlencode","data@%s"%file_path,
            "-d","graph=%s"%urllib.quote(graph_uri),
            "-d","mime-type=%s"%content_format,
            epr]
   p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   output, err = p.communicate()
   ret = p.poll()
   if ret <> 0:
       raise Exception, "error asserting %s in graph %s\n%s\n%s"%\
                        (file_path,graph_uri,output,err)
   return ret

def assert_data_in_graph(graph_uri,data,epr,content_format,flushGraph=False,queryEpr=None,api_key=None):
   if flushGraph:
       subprocess.check_call(["curl","-X","DELETE","%s%s"%(epr,graph_uri)])
       time.sleep(1)
       if queryEpr:
            sq=SPARQL(queryEpr)
            assert sq.count_in_graph(graph_uri) == 0
   return assert4s(data,epr,graph_uri,content_format,api_key=api_key)


def assert4s(data,epr,graph,contenttype,api_key=None):
    try:
        p = {'graph': graph,'data': data,'mime-type' : contenttype }
        if not api_key:
            params["apikey"] = api_key
        params = urllib.urlencode(p)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(epr,params)
        request.get_method = lambda: 'POST'
        url = opener.open(request)
        return url.read()
    except Exception, e:
        raise e

def update4s(update,epr,api_key=None):
    try:
        p = {'update': update.encode("utf-8")}
        if api_key:
            p["apikey"] = api_key
        params = urllib.urlencode(p)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(epr,params)
        request.get_method = lambda: 'POST'
        url = opener.open(request)
        return url.read()
    except Exception, e:
        traceback.print_exc(file=sys.stdout)
        raise e
