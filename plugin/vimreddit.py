# -*- coding: utf-8 -*-

import HTMLParser
import json
import vim
import webbrowser

REDDIT_URL = 'http://www.reddit.com/r/programming/hot.json'

def bufwrite(string):
    b = vim.current.buffer

    # Never write more than two blank lines in a row
    if not string.strip() and not b[-1].strip() and not b[-2].strip():
        return

    # Vim must be given UTF-8 rather than unicode
    if isinstance(string, unicode):
        string = string.encode('utf-8', errors='replace')

    # Code block markers for syntax highlighting
    if string and string[-1] == unichr(160).encode('utf-8'):
        b[-1] = string
        return

    if not b[0]:
        b[0] = string
        return

    if not b[0]:
        b[0] = string
    else:
        b.append(string)

def vim_reddit():
    vim.command('edit .reddit')
    vim.command('setlocal noswapfile')
    vim.command('setlocal buftype=nofile')

    bwrite('/r/programming (http://www.reddit.com/r/programming)')
    bwrite('')

    items = json.loads(urllib2.urlopen(REDDIT_URL).read())
    for index, item in enumerate(items.data.children):
        line_1 = index + '. ' + item['title'] + '(' + item['domain'] + ')'
        line_2 = item['score'] + ' points by ' + \
                 item['author'] + ' | ' + item['num_comments'] + ' comments'
        bwrite(line_1)
        bwrite(line_2)
