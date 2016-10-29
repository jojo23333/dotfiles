call plug#begin('~/.vim/plugged')

"copy from internet

set nocompatible                 "去掉有关vi一致性模式，避免以前版本的bug和局限    

set number
set relativenumber                                    "显示行号

set guifont=Luxi/Mono/9   " 设置字体，字体名称和字号

filetype on                              "检测文件的类型     

set history=1000                  "记录历史的行数

set cindent                             "（cindent是特别针对 C语言语法自动缩进）

set smartindent                    "依据上面的对齐格式，智能的选择对齐方式，对于类似C语言编写上有用   

set tabstop=4                        "设置tab键为4个空格，

set ai!                            " 设置自动缩进 
   
set vb t_vb=                            "当vim进行编辑时，如果命令错误，会发出警报，该设置去掉警报       

set ruler                                  "在编辑过程中，在右下角显示光标位置的状态行     

set incsearch                        "在程序中查询一单词，自动匹配单词的位置；如查询desk单词，当输到/d时，会自动找到第一个d开头的单词，当输入到/de时，会自动找到第一个以ds开头的单词，以此类推，进行查找；当找到要匹配的单词时，别忘记回车 

set backspace=2           " 设置退格键可用

"end

"synatax highlighting methods

" 主题 solarized
Plug 'altercation/vim-colors-solarized'
"let g:solarized_termcolors=256
let g:solarized_termtrans=1
let g:solarized_contrast="normal"
let g:solarized_visibility="normal"
" 主题 molokai
Plug 'tomasr/molokai'
let g:molokai_original = 1
" 配色方案
set background=dark
set t_Co=256

    "colorscheme solarized
    colorscheme molokai
    "colorscheme phd


"press F5 to open or close nerdtree
nmap <F5> :NERDTreeToggle<cr>
"press F6 to open or close tagslist
nmap <F6> :TlistToggle<cr>

"automatically starts up nerdtree
"autocmd vimenter * NERDTree
"automatically close vim
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif

"Plug 'Valloric/YouCompleteMe'
Plug 'jiangmiao/auto-pairs'
Plug 'scrooloose/nerdcommenter'
Plug 'scrooloose/nerdtree'
"Plug 'rdnetto/YCM-Generator', { 'branch': 'stable'}
Plug 'Shougo/neocomplete.vim'
Plug 'vim-scripts/taglist.vim'

"Note: This option must be set in .vimrc(_vimrc).  NOT IN .gvimrc(_gvimrc)!
" Disable AutoComplPop.
let g:acp_enableAtStartup = 0
" Use neocomplete.
let g:neocomplete#enable_at_startup = 1
" Use smartcase.
let g:neocomplete#enable_smart_case = 1
" Set minimum syntax keyword length.
let g:neocomplete#sources#syntax#min_keyword_length = 3
let g:neocomplete#lock_buffer_name_pattern = '\*ku\*'

" Define dictionary.
let g:neocomplete#sources#dictionary#dictionaries = {
    \ 'default' : '',
    \ 'vimshell' : $HOME.'/.vimshell_hist',
    \ 'scheme' : $HOME.'/.gosh_completions'
        \ }

" Define keyword.
if !exists('g:neocomplete#keyword_patterns')
    let g:neocomplete#keyword_patterns = {}
endif
let g:neocomplete#keyword_patterns['default'] = '\h\w*'

" Plugin key-mappings.
inoremap <expr><C-g>     neocomplete#undo_completion()
inoremap <expr><C-l>     neocomplete#complete_common_string()

" Recommended key-mappings.
" <CR>: close popup and save indent.
inoremap <silent> <CR> <C-r>=<SID>my_cr_function()<CR>
function! s:my_cr_function()
  return (pumvisible() ? "\<C-y>" : "" ) . "\<CR>"
  " For no inserting <CR> key.
  "return pumvisible() ? "\<C-y>" : "\<CR>"
endfunction
" <TAB>: completion.
inoremap <expr><TAB>  pumvisible() ? "\<C-n>" : "\<TAB>"
" <C-h>, <BS>: close popup and delete backword char.
inoremap <expr><C-h> neocomplete#smart_close_popup()."\<C-h>"
inoremap <expr><BS> neocomplete#smart_close_popup()."\<C-h>"
" Close popup by <Space>.
"inoremap <expr><Space> pumvisible() ? "\<C-y>" : "\<Space>"

" AutoComplPop like behavior.
"let g:neocomplete#enable_auto_select = 1

" Shell like behavior(not recommended).
"set completeopt+=longest
"let g:neocomplete#enable_auto_select = 1
"let g:neocomplete#disable_auto_complete = 1
"inoremap <expr><TAB>  pumvisible() ? "\<Down>" : "\<C-x>\<C-u>"

" Enable omni completion.
autocmd FileType css setlocal omnifunc=csscomplete#CompleteCSS
autocmd FileType html,markdown setlocal omnifunc=htmlcomplete#CompleteTags
autocmd FileType javascript setlocal omnifunc=javascriptcomplete#CompleteJS
autocmd FileType python setlocal omnifunc=pythoncomplete#Complete
autocmd FileType xml setlocal omnifunc=xmlcomplete#CompleteTags

" Enable heavy omni completion.
if !exists('g:neocomplete#sources#omni#input_patterns')
  let g:neocomplete#sources#omni#input_patterns = {}
endif
"let g:neocomplete#sources#omni#input_patterns.php = '[^. \t]->\h\w*\|\h\w*::'
"let g:neocomplete#sources#omni#input_patterns.c = '[^.[:digit:] *\t]\%(\.\|->\)'
"let g:neocomplete#sources#omni#input_patterns.cpp = '[^.[:digit:] *\t]\%(\.\|->\)\|\h\w*::'

" For perlomni.vim setting.
" https://github.com/c9s/perlomni.vim
let g:neocomplete#sources#omni#input_patterns.perl = '\h\w*->\h\w*\|\h\w*::'

let Tlist_Ctags_Cmd = '/usr/bin/ctags'
let Tlist_Show_One_File = 1            "不同时显示多个文件的tag，只显示当前文件的
let Tlist_Exit_OnlyWindow = 1          "如果taglist窗口是最后一个窗口，则退出vim
let Tlist_Use_Right_Window = 1         "在右侧窗口中显示taglist窗口
let Tlist_Exit_OnlyWindow = 1          "只剩taglist时自动退出

call plug#end()
