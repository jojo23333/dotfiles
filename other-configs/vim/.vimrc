call plug#begin('~/.vim/plugged')

"synatax highlighting methods
Plug 'altercation/vim-colors-solarized'
Plug 'tomasr/molokai'

Plug 'Valloric/YouCompleteMe', { 'do': './install.py --clang-completer'}
Plug 'jiangmiao/auto-pairs'
Plug 'scrooloose/nerdcommenter'
Plug 'scrooloose/nerdtree'
"Plug 'rdnetto/YCM-Generator', { 'branch': 'stable'}
"Plug 'Shougo/neocomplete.vim'
Plug 'vim-scripts/taglist.vim'
Plug 'scrooloose/syntastic'
Plug 'tpope/vim-fugitive'

call plug#end()


"""""""""""""""""""""
"""vim global settings
"""""""""""""""""""""
set nocompatible                 "去掉有关vi一致性模式，避免以前版本的bug和局限    
set number
set relativenumber               "显示行号
set guifont=Luxi/Mono/9          " 设置字体，字体名称和字号
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

""""""""""""""""""""""""""""
"""neocomplete settings
""""""""""""""""""""""""""""
"""https://github.com/Shougo/neocomplete.vim confiurations settings

""""""""""""""""""""""""""""
"""NerdTreeSettings
""""""""""""""""""""""""""""
"press F5 to open or close nerdtree
nmap <F5> :NERDTreeToggle<cr>
"automatically starts up nerdtree
"autocmd vimenter * NERDTree
"automatically close vim
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif

""""""""""""""""""""""""""""
"""CTags settings
""""""""""""""""""""""""""""
"press F6 to open or close tagslist
nmap <F6> :TlistToggle<cr>
let Tlist_Ctags_Cmd = '/usr/bin/ctags'
let Tlist_Show_One_File = 1            "不同时显示多个文件的tag，只显示当前文件的
let Tlist_Exit_OnlyWindow = 1          "如果taglist窗口是最后一个窗口，则退出vim
let Tlist_Use_Right_Window = 1         "在右侧窗口中显示taglist窗口
let Tlist_Exit_OnlyWindow = 1          "只剩taglist时自动退出

""""""""""""""""""""""""""""
"""Highlighting settings
""""""""""""""""""""""""""""
let g:molokai_original = 1
" 配色方案
"let g:solarized_termcolors=256
let g:solarized_termtrans=1
let g:solarized_contrast="normal"
let g:solarized_visibility="normal"
set background=dark
set t_Co=256
    "colorscheme solarized
    colorscheme molokai
    "colorscheme phd



"""""""""""""""""""""""""""""
"""You Complete Me settings
"""""""""""""""""""""""""""""
let g:ycm_global_ycm_extra_conf = '/home/jojo/.vim/plugged/YouCompleteMe/third_party/ycmd/cpp/ycm/.ycm_extra_conf.py'
" show diagnostic list when <c-l>
nnoremap <c-l> :YcmDiags<CR>
let g:ycm_confirm_extra_conf = 0
let g:ycm_autoclose_preview_window_after_completion = 1
let g:ycm_show_diagnostics_ui = 0
" Ycm Fixit feature
nnoremap <c-h> :YcmCompleter FixIt<CR>
"let g:ycm_collect_identifiers_from_comments_and_strings = 1
" Used for choose python version
"let g:ycm_python_binary_path = '/usr/bin/python3'
let g:ycm_key_detailed_diagnostics = ''








