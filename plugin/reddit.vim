if !has('python3')
  echo 'vim-reddit requires Vim compiled with +python3!'
  finish
endif

execute 'python3 import sys'
execute "python3 sys.path.append(r'" . expand("<sfile>:p:h")  . "')"
execute "python3 from vimreddit import vim_reddit, vim_reddit_link"

command! Reddit python3 vim_reddit(<f-args>)

au! BufRead,BufNewFile *.reddit set filetype=reddit
