if exists('b:current_syntax')
  finish
endif

syn match Header /\/r\/programming \(http:\/\/www.reddit.com\/r\/programming\)/
highlight Title ctermfg=208 guifg=#ff6600

" highlight link info as a comment
syn match Comment /\d points by .* | \d comments/

let b:current_syntax = 'reddit'
