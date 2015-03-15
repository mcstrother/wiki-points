# Getting Started #

  1. Install Python 2.6+
  1. Check out the source code
  1. Download the source code of the wikitools project (http://code.google.com/p/python-wikitools/). Put it in a folder wiki-points/wikitools.
  1. Run wiki\_points.py. It currently just shows you that one of the first articles I ever edited was "Mac McGarry" (I happen to have founded that article) and that it has been view 21,344 times since I edited it.

You can also try something like this from the interpreter:
```
>>> from wiki_points import get_pageviews_since_date
>>> from datetime import date
>>> start = date(2011, 3, 13)
>>> import wikitools
>>> wikipedia = wikitools.wiki.Wiki(url="http://en.wikipedia.org/w/api.php")
>>> article = wikitools.page.Page(wikipedia, title="Wikipedia")
>>> get_pageviews_since_date(article, start)
(a very big number)
```