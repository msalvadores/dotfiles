c = get_config()
c.InteractiveShellApp.exec_lines = [
'from http_sparql_client import *',
'import os',
'local = SPARQL("http://localhost:9000/sparql/")',
'prod_CARE = SPARQL(os.environ[\'SPARQL_BP_PRD\'])',
'stage = SPARQL(os.environ[\'SPARQL_BP_STG\'])',
'print "prod_CARE.epr=%s"%prod_CARE.epr',
'print "stage.epr=%s"%stage.epr',
'print "local.epr=%s"%local.epr'
]
