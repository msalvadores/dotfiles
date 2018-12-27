call plug#begin('~/.local/share/nvim/plugged')
Plug 'junegunn/vim-easy-align'
Plug 'scrooloose/nerdtree'
Plug 'vim-airline/vim-airline'
Plug 'easymotion/vim-easymotion'
Plug 'vim-syntastic/syntastic'
Plug 'airblade/vim-gitgutter'
Plug 'mhartington/oceanic-next'
Plug 'bfredl/nvim-ipy'
Plug 'scrooloose/nerdcommenter'
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
Plug 'junegunn/fzf.vim'
Plug 'mkitt/tabline.vim'
Plug 'neovimhaskell/haskell-vim'
Plug 'Alok/notational-fzf-vim'

let g:fzf_action = {
      \ 'ctrl-s': 'split',
      \ 'ctrl-v': 'vsplit',
      \ 'ctrl-t': 'tab split'
      \ }
nnoremap <c-p> :FZF<cr>
let $FZF_DEFAULT_COMMAND = 'ag -f -l -g "" --ignore-dir=venv'
call plug#end()

 
syntax enable
filetype plugin indent on

set noeb " disable error bell
set novb " don't blink the screen when there is an error
set backupext=.bak  " Append `.bak' to backups
set nocompatible
set number
set smartindent
set tabstop=4
set shiftwidth=4
set expandtab
set clipboard=unnamed

autocmd FileType go setlocal noexpandtab shiftwidth=4 tabstop=4 softtabstop=4 nolist
autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab

:nmap \f :echo @%<CR>
:nmap \t :tabnew<CR>
:nmap \p :set paste!<CR>
:nmap \l :setlocal number!<CR>
:nmap \t <ESC>:tabnew<CR>ww
:nmap \q <ESC>:q<CR>
:nmap \w <ESC>:w<CR>
:imap \w <ESC>:w<CR>

"insert mode escape via jj
:imap jj <Esc>

"linewise up/down
:nmap j gj
:nmap k gk

"nerd tree ctrl-d toggle
map \d :execute 'NERDTreeToggle ' . getcwd()<CR>
let NERDTreeIgnore = ['\.pyc$','\.class$','\.swp$']

set wildignore+=*.swp,*.pyc,*.class
set wildignore+=python_envs
set wildignore+=build
set wildignore+=assets

"search across files in current project - selected text
"command GF :execute 'vimgrep /'.expand('<cword>').'/j '.expand(' **/*.c **/*.h **/*.java **/*.py **/*.js **/*.html **/*.rb') | copen

" Center display line after searches "
nnoremap n   nzz
nnoremap N  Nzz
nnoremap *  *zz
nnoremap #  #zz
nnoremap g* g*zz
nnoremap g# g#z

" Search for current word in new window
:nmap \v :let @/=expand("<cword>")<Bar>split<Bar>normal n<CR>
:nmap \V :let @/='\<'.expand("<cword>").'\>'<Bar>split<Bar>normal n<CR>

"delete no-yank
nnoremap R "_d

"search options
set hlsearch
set incsearch
set ignorecase
set smartcase
:nmap \ns :nohlsearch<CR>

colorscheme OceanicNext

if has('statusline')
    "set laststatus=2
    set laststatus=0

	" Broken down into easily includeable segments
	set statusline=%<%f\    " Filename
	set statusline+=%w%h%m%r " Options
	set statusline+=\ [%{getcwd()}]          " current dir
	set statusline+=%=%-14.(%l,%c%V%)\ %p%%  " Right aligned file nav info
endif

"ruby indentation
autocmd BufNewFile,BufRead *.rb set tabstop=2
autocmd BufNewFile,BufRead *.rb set shiftwidth=2

"ask for reload
:au FileChangedShell * echo "Warning: File changed on disk"

set backspace=2 " make backspace work like most other apps

"update syntastic errors on save
let g:syntastic_always_populate_loc_list=1

"low timeout for escaping
set timeoutlen=1000 ttimeoutlen=50
set cursorline

inoremap  <Up>     <NOP>
inoremap  <Down>   <NOP>
inoremap  <Left>   <NOP>
inoremap  <Right>  <NOP>
noremap   <Up>     <NOP>
noremap   <Down>   <NOP>
noremap   <Left>   <NOP>
noremap   <Right>  <NOP>

"remove trailing in python and ruby
autocmd BufWritePre *.py :%s/\s\+$//e
autocmd BufWritePre *.rb :%s/\s\+$//e
autocmd BufWritePre *.sh :%s/\s\+$//e
autocmd BufWritePre *.sql :%s/\s\+$//e

":vmap R :!psql -U lexigram -d $PSDB -e<enter>
:vmap R :!psql $VIMPSDB -e<enter>

set timeoutlen=500 ttimeoutlen=0

map <Leader>r ?-- start<CR>jV/;<CR>R\ns

map <Leader>c <Esc>1gtGGi

map [q :cprevious<CR>
map ]q :cnext<CR>

map <c-l> <Esc>:BLines<CR>
map <c-L> <Esc>:Lines<CR>

" The Silver Searcher
if executable('ag')
  " Use ag over grep
  set grepprg=ag\ --nogroup\ --nocolor

  " Use ag in CtrlP for listing files. Lightning fast and respects .gitignore
  let g:ctrlp_user_command = 'ag %s -l --nocolor -g ""'

  " ag is fast enough that CtrlP doesn't need to cache
  let g:ctrlp_use_caching = 0
endif

" bind K to grep word under cursor
nnoremap K :grep! "\b<C-R><C-W>\b"<CR>:cw<CR>

" terminal maps
:tnoremap <Esc> <C-\><C-n>
:tnoremap jj <C-\><C-n>

"Ipy
let g:nvim_ipy_perform_mappings = 0
map <silent> <c-s>   <Plug>(IPy-Run)
hi CursorLine term=bold cterm=bold guibg=Grey40

nnoremap <tab> :call fzf#vim#ag(expand('<cword>'))<CR>
"map <CR> :tabnew<CR>:Ag 
"
let g:nv_search_paths = ['~/Dropbox/notes']
let g:nv_use_short_pathnames = 1
let g:nv_default_extension = '.md'

"paste end of line with ,
nmap , $p
