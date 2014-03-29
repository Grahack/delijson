delijson
========

Parse HTML exports of Delicious bookmarks to create JSON reports.

Github repo: <https://github.com/Grahack/delijson>

Usage
=====

`./delijson.py delicious_export.html [stats]`

Where `[stats]` is a list of `.json` files you want to create among:

* `partition`, for a list of tag combinations which separate links from each
  others (like a [math partition](https://en.wikipedia.org/wiki/Partition_of_a_set).
  Also you have the links and their count.
* `tags`, for a list of tags and the number of links that are tagged at least
  with this tag.
* `relations`, for a list of pairs of tags (as a string like `tag1 tag2`, so
  do not use space in your tags!) and the number of links in which they appear
  both.

So if you want the first and the last:  

`./delijson.py delicious_export.html partition relations`

Sorry
=====

No nice Python packaging! But I accept pull requests.

