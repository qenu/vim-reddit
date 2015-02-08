if exists('b:current_syntax')
  finish
endif

syn match Header /^\/r\/programming.*$/
highlight Header ctermfg=208 guifg=#ff6600

" highlight link info as a comment
syn match Comment /\d points by .* | \d comments/

let b:current_syntax = 'reddit'
