#!/usr/bin/env python3
"""
Read-only reddit mirror of comments, submissions and upvoted posts; everything except saved
"""
from orger import Mirror
from orger.inorganic import node, link, Quoted
from orger.common import dt_heading


from my.reddit import upvoted, submissions, comments


class RedditAllView(Mirror):
    def get_items(self) -> Mirror.Results:
        yield node(
            'Submissions',
            children=[node( # TODO can also be iterable?
                dt_heading(s.created, link(title=s.title, url=s.url)),
                body=Quoted(s.text),
            ) for s in submissions()]
        )
        yield node(
            'Comments', # todo parent thread??
            children=[node(
                dt_heading(c.created, link(title=c.url, url=c.url)),
                body=Quoted(c.text),
            ) for c in comments()],
        )
        yield node(
            'Upvoted',
            children=[node(
                dt_heading(u.created, link(title=u.title, url=u.url)),
                body=Quoted(u.text),
             ) for u in upvoted()]
        )


if __name__ == '__main__':
    RedditAllView.main()

# todo not sure if for reddit worth converting bodies from md to org? I guess quoting is ok for now?
