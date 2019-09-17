#!/usr/bin/env python3
from orger import Interactive
from orger.inorganic import node, link, org_dt
from orger.org_utils import todo, dt_heading

from typing import NamedTuple, List, Any, Iterable, Tuple, Optional
import logging

from my.reddit import Save, get_saves, get_logger as get_reddit_logger # type: ignore

from kython.knetwork import is_alive

# TODO mm, yeah, perhaps favoriting date makes a bit more sense...
# I guess, sort of reasonable to test at rendering time

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


# TODO is_alive should handle DELETED comments...
# ah, sometimes it's [removed]
# TODO maybe, track that in reddit provider? since we have all version of saved items over time
class RedditView(Interactive):
    def get_items(self):
        for s in get_saves(all_=True, parallel=False):
            yield s.sid, node(
                # need to make heading lazy due to is_alive
                heading=lambda s=s: dt_heading(
                    s.save_dt,
                    ('' if is_alive(s.url) else '[#A] *DEAD* ') + link(title=s.title, url=s.url) + f' /r/{s.subreddit}'
                ),
                body=s.text,
            )

if __name__ == '__main__':
    # setup_logzero(get_reddit_logger(), level=logging.DEBUG)
    RedditView.main()

# ok, so far:
# adding -- tracked via json state; kinda ok.
# hmmm! just keep reddit bookmarks intact! whatever, serously!
# one reason for using reddit ('native') favoriting is that you get more metadata for free
# hypothesis and instapaper views do not update state and clear the file before writing
# reddit view tracks the state and appends only
