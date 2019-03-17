#!/usr/bin/env python3
from multiprocessing import Pool
from typing import NamedTuple, List, Any, Iterable, Tuple, Optional, Collection
import logging

from my.reddit import Save, get_saves, get_logger as get_reddit_logger # type: ignore

from kython.org_tools import link as org_link
from kython.knetwork import is_alive
from kython.klogging import setup_logzero

from org_view import OrgViewAppend, OrgWithKey
from org_utils import OrgTree, as_org

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
# TODO maybe, track that in reddit provider? since we have all version of saved items over time
class RedditView(OrgViewAppend):
    # pylint: disable=unsubscriptable-object
    def get_items(self) -> Collection[OrgWithKey]:
        return [(
            s.sid,
            # need to make it lazy due to is_alive
            OrgTree(lambda s=s: as_org( # type: ignore
                    created=s.save_dt,
                    heading=('' if is_alive(s.url) else '[#A] *DEAD* ') + org_link(title=s.title, url=s.url) + f' /r/{s.subreddit}',
                    body=s.text,
            ))
        ) for s in get_saves(all_=True)]


def main():
    # setup_logzero(get_reddit_logger(), level=logging.DEBUG)

    RedditView(
        logger_tag='reddit-view',
        file_header=f"# AUTOGENERATED BY {__file__}",
    ).main(
        default_to='reddit.org',
        default_state='reddit.json',
    )

if __name__ == '__main__':
    main()

# ok, so far:
# adding -- tracked via json state; kinda ok.
# hmmm! just keep reddit bookmarks intact! whatever, serously!
# one reason for using reddit ('native') favoriting is that you get more metadata for free
# hypothesis and instapaper views do not update state and clear the file before writing
# reddit view tracks the state and appends only
