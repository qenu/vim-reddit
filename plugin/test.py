import json
import urllib.request


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


output = json.loads(read_url(redditurl('all')))

print(output)
