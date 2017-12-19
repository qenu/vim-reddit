import json
from urllib import URLopener
from urllib import urlopen
from urllib import FancyURLopener

class VIMRedditOpener(FancyURLopener):
    version = 'Python/vim-reddit'

def redditurl(subreddit):
    return 'http://www.reddit.com/r/' + subreddit + '/hot.json'

def read_url(url):
    response = urllib.request.urlopen(url)
    return str(response.read())

theopener = VIMRedditOpener()
page = theopener.open(redditurl('all'))
jsonoutput = page.read()

print(jsonoutput)
