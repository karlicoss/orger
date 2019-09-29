#!/usr/bin/env python3
from orger import InteractiveView
from orger.inorganic import node, link
from orger.common import todo, dt_heading

import logging

from my.reddit import get_saves

# TODO get rid of this?
from kython.knetwork import is_alive


class RedditView(InteractiveView):
    def get_items(self):
        for s in get_saves():
            yield s.sid, node(
                # need to make heading lazy due to is_alive
                heading=lambda s=s: dt_heading(
                    s.created,
                    ('' if is_alive(s.url) else '[#A] *DEAD* ') + link(title=s.title, url=s.url) + f' /r/{s.subreddit}'
                ),
                body=s.text,
            )

if __name__ == '__main__':
    RedditView.main()


# TODO is_alive should handle DELETED comments...
# ah, sometimes it's [removed]
# TODO maybe, track that in reddit provider? since we have all version of saved items over time

# TODO actually might be useful to store forever a read only version...
# eh, turned out easier to make it lazy..
# def get_saves_with_state():
#     # TODO don't query for dead so often. We actually only want to get it for new items..
#     saves = get_saves(all_=False)
#     with Pool() as p:
#         res = p.map(_helper, saves)
#     dead = [r for r, s in res if not s]
#     # if len(dead) / (len(saves) + 1) > 0.3:
#     #     raise RuntimeError('something must be wrong with reddit! bailing')
#     return res

