# vim-reddit

Browse [reddit](https://www.reddit.com/) inside Vim!

Heavily inspired (and forked) from [vim-hackernews](https://github.com/ryanss/vim-hackernews).
![subreddit home](https://raw.githubusercontent.com/mnpk/vim-reddit/master/vim-reddit-home.png)

## Usage

* Open the front page of a subreddit with `:Reddit [subreddit]` or `:Reddit` to open r/all.
* Press lowercase `o` to open links in Vim. (Images/videos will still open in a web browser since...well you can't view images/videos in a terminal.)
* Press uppercase `O` to open links in the default web browser
* Press lowercase `c` to view the comments of a reddit post in your browser.
* Press lowercase `u` to go back (or whatever you've remapped `undo` to)
* Press `Ctrl+r` to go forward (or whatever you're remapped `redo` to)
* Execute the `:bd` command to close and remove the reddit buffer

## Installation

##### Plug (Recommended)

```
Plug 'joshhartigan/vim-reddit'
```

##### Pathogen

```bash
git clone https://github.com/joshhartigan/vim-reddit ~/.vim/bundle/vim-reddit
```

##### Vundle, vim-plug and friends

```
Plugin 'joshhartigan/vim-reddit'
```
