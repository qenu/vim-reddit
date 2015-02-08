if !has('python')
  echo 'vim-reddit requires Vim compiled with +python!'
  finish
endif

execute 'python import sys'
execute "python sys.path.append(r'" . expand("<sfile>:p:h")  . "')"
execute "python from vimreddit import vim_reddit, vim_redd_link"

command! VimReddit python vim_reddit()

au! BufRead,BufNewFile *.reddit set filetype=reddit
