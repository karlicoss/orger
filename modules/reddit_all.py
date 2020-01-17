#!/usr/bin/env python3
"""
Read-only reddit mirror of comments, submissions and upvoted posts; everything except saved
"""

from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading


from my.reddit import upvoted, submissions, comments


# TODO convert bodies from markdown to org-mode
class RedditAllView(StaticView):
    def get_items(self):
        yield node(
            'Submissions',
            children=[node( # TODO can also be iterable?
                dt_heading(s.created, link(title=s.title, url=s.url)),
                body=s.text,
            ) for s in submissions()]
        )
        yield node(
            'Comments', # TODO parent thread??
            children=[node(
                dt_heading(c.created, link(title=c.url, url=c.url)),
                body=c.text,
            ) for c in comments()],
        )
        yield node(
            'Upvoted',
            children=[node(
                dt_heading(u.created, link(title=u.title, url=u.url)),
                body=u.text,
             ) for u in upvoted()]
        )


if __name__ == '__main__':
    RedditAllView.main()
