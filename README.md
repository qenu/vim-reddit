# vim-reddit (With Python3 Support) (now without Fuck Yeah Markdown API)

Browse [reddit](https://www.reddit.com/) inside Vim!

Forked from [joshhartigan's vim-reddit plugin](https://github.com/joshhartigan/vim-reddit) with added Python3 support and more. 

Then Forked from [DougBeney/vim-reddit](https://github.com/DougBeney/vim-reddit) replacing the markdown api with some mediocre code.

![subreddit home](https://raw.githubusercontent.com/mnpk/vim-reddit/master/vim-reddit-home.png)
**New Features:**

- Open the comments of a post in your browser by pressing c
- Image and video links open in your web browser instead of attempting to open in your terminal
- You can now open links that are inside reddit posts.
- You can now simply type :Reddit with no parameters and you will be able to view r/all


## Usage

* Open the front page of a subreddit with `:Reddit [subreddit]` or `:Reddit` to open r/all.
* Press lowercase `o` to open links in Vim. (Images/videos will still open in a web browser since...well you can't view images/videos in a terminal.)
* Press uppercase `O` to open links in the default web browser
* Press lowercase `c` to view the comments of a reddit post in your browser.
* Press lowercase `u` to go back (or whatever you've remapped `undo` to)
* Press `Ctrl+r` to go forward (or whatever you're remapped `redo` to)
* Execute the `:bd` command to close and remove the reddit buffer

## Installation

##### Pathogen

```bash
git clone https://github.com/qenu/vim-reddit ~/.vim/bundle/vim-reddit
```

i have no idea how the others work, im sorry 
