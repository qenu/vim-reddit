# -*- coding: utf-8 -*-

import vim
import textwrap
import json
import webbrowser
import urllib.request
import re

MARKDOWN_URL = 'http://fuckyeahmarkdown.com/go/?read=1&u='
urls = [None] * 1000  # urls[index]: url of link at index


def redditurl(subreddit):
    return 'http://www.reddit.com/r/' + subreddit + '/hot.json'


def read_url(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Python/vim-reddit'
        }
    )

    f = urllib.request.urlopen(req)

    return f.read().decode('utf-8')


def bufwrite(string):
    b = vim.current.buffer

    # Never write more than two blank lines in a row
    if not string.strip() and not b[-1].strip() and not b[-2].strip():
        return

    # Vim must be given UTF-8 rather than unicode
    if isinstance(string, str):
        string = string.encode('utf-8', errors='replace')

    # Code block markers for syntax highlighting
    if string and string[-1] == chr(160).encode('utf-8'):
        b[-1] = string
        return

    if not b[0]:
        b[0] = string
        return

    if not b[0]:
        b[0] = string
    else:
        b.append(string)


def vim_reddit(sub):
    vim.command('edit .reddit')
    vim.command('setlocal noswapfile')
    vim.command('setlocal buftype=nofile')

    bufwrite('    ┌─o')
    bufwrite(' ((•  •))  r e d d i t')
    bufwrite(' http://www.reddit.com/r/' + sub)
    bufwrite('')

    items = json.loads(read_url(redditurl(sub)))
    for i, item in enumerate(items['data']['children']):
        item = item['data']
        try:
            # surround shorter numbers (e.g. 9) with padding
            # to align with longer numbers
            index = (2 - len(str(i + 1))) * ' ' + str(i + 1) + '. '

            line_1 = index + item['title'] + ' (' + item['domain'] + ')'
            line_2 = '    ' + str(item['score']) + ' points, by ' + \
                     item['author'] + ' | ' + str(item['num_comments']) + \
                     ' comments'
            bufwrite(line_1)
            bufwrite(line_2)
            bufwrite('')

            urls[i + 1] = item['url']
        except KeyError:
            pass


def render_url(url):
    vim.command('edit .reddit')
    content = read_url(MARKDOWN_URL + url)
    for i, line in enumerate(content.split('\n')):
        if not line:
            bufwrite('')
            continue
        line = textwrap.wrap(line, width=80)
        for wrap in line:
            bufwrite(wrap)


def is_media_link(url):
    media_matches = [
        'redditmedia.com',
        'reddit.com/video/',
        'imgur.com',
        'gfycat.com',
        r'\.(gif|jpg|jpeg|tiff|png|svg)$',
    ]
    for media_match in media_matches:
        if re.search(media_match, url):
            return True
    return False


def vim_reddit_link(in_browser=False):
    # Checking if they are viewing the
    # home page or are reading a post
    # by using the alien antenna as a
    # reference.
    b = vim.current.buffer
    if '┌─o' in b[0]:
        viewing_home_page = True
    else:
        viewing_home_page = False

    line = vim.current.line

    if viewing_home_page:
        # User is not viewing a webpage in VIM
        # This means that they are viewing a sub's
        # hot feed.

        regexp = re.compile(r'\d+\.')
        if regexp.search(line) is not None:
            id = line.split()[0].replace('.', '')

            if is_media_link(urls[int(id)]):
                in_browser = True

            if in_browser:
                browser = webbrowser.get()
                browser.open(urls[int(id)])
                return
            render_url(urls[int(id)])
            return
        print('vim-reddit error: could not parse item')
    else:
        # User is viewing a webpage.
        # In this case we will take a look at the
        # line they are trying to edit and use
        # some regex magic to find a URL.
        URL_REGEX =\
            r'(http|https)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?'

        URLS_IN_LINE = re.search(URL_REGEX, line)
        if URLS_IN_LINE:
            # The first URL in a line
            URL_IN_LINE = URLS_IN_LINE[0]

            # If URL is to an image/video,
            # force open in browser.
            if is_media_link(URL_IN_LINE):
                in_browser = True

            if in_browser:
                browser = webbrowser.get()
                browser.open(URL_IN_LINE)
            else:
                render_url(URL_IN_LINE)
