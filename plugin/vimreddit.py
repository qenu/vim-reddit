# -*- coding: utf-8 -*-

import vim
import textwrap
import json
import webbrowser
import urllib.request
import re
import time

post_results = [None] * 1000  # The posts for the chosen subreddit

# MARKDOWN_URL = 'http://fuckyeahmarkdown.com/go/?read=1&u=' # WELL THIS ISN'T WORKING ANYMORE

def redditurl(subreddit):
    return 'http://www.reddit.com/r/' + subreddit + '/hot.json'


def read_url(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
        }
        )
    f = urllib.request.urlopen(req)

    return f.read().decode('utf-8')

def bulkwrite(string, *, prepend = ''):
    # bufwrite in bulks
    for line in string.split('\n'):
        if not line:
            bufwrite('')
            continue
        line = textwrap.wrap(prepend + line, width=80)
        for wrap in line:
            bufwrite(wrap)

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

def vim_reddit(sub="all"):
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

            post_results[i + 1] = {
                "url": item['url'],
                "permalink": "https://reddit.com" + item['permalink'],
            }
        except KeyError:
            pass


def render_url(url, filename='.reddit', newtab=False):
    # New-tab and filename functionality is now possible
    # but not implemented anywhere else in this plugin.
    if newtab:
        vim.command('tabnew')
    vim.command('edit ' + filename)

    # this is some temp solution since fuck yeah markdown is down
    # :< sorry it sucks

    content = json.loads(read_url(url[:-1]+'.json'))
    post, comment = content
    post = post['data']['children'][0]['data']

    bufwrite(post['title'])
    bufwrite('('+post['domain']+' | '+post['author_fullname']+')')
    bufwrite('')
    bulkwrite(post['selftext'])
    bufwrite('')
    bufwrite('--- comments section ---')
    bufwrite('')

    comments = comment['data']['children']
    for comment in comments:
        if comment['kind'] == 't1':
            bulkwrite(comment['data']['body'])
            if len(comment['data']['replies']) != 0:
                replies = comment['data']['replies']['data']['children']
                for reply in replies:
                    if reply['kind'] == 't1':
                        bulkwrite(reply['data']['body'], prepend='    ')
        bufwrite('')


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


def render_frontpage_item(in_browser, parameter='url'):
    regexp = re.compile(r'\d+\.')
    line = vim.current.line
    if regexp.search(line) is not None:
        id = line.split()[0].replace('.', '')

        the_url = post_results[int(id)][parameter]

        if is_media_link(the_url):
            in_browser = True

        if in_browser:
            browser = webbrowser.get()
            browser.open(the_url)
            return
        render_url(the_url)
        return
    print('vim-reddit error: could not parse item')


def vim_reddit_comments_link():
    b = vim.current.buffer
    if '┌─o' in b[0]:
        viewing_home_page = True
    else:
        viewing_home_page = False

    if viewing_home_page:
        render_frontpage_item(True, 'permalink')


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

    if viewing_home_page:
        render_frontpage_item(in_browser)
    else:
        # User is viewing a webpage.
        # In this case we will take a look at the
        # line they are trying to edit and use
        # some regex magic to find a URL.
        URL_REGEX =\
            r'(http|https)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?'

        line = vim.current.line
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

