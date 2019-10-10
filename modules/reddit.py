#!/usr/bin/env python3
from orger import InteractiveView
from orger.inorganic import node, link
from orger.common import dt_heading

from my.reddit import get_saves

class RedditView(InteractiveView):
    def get_items(self):
        for s in get_saves():
            yield s.sid, node(
                # need to make heading lazy due to is_alive
                heading=lambda s=s: dt_heading(
                    s.created,
                    ('[#A] *DEAD*' if self.is_dead_url(s.url) else '') + link(title=s.title, url=s.url) + f' /r/{s.subreddit}'
                ),
                body=s.text,
            )

    def is_dead_url(self, url: str) -> bool:
        assert self.cmdline_args is not None
        if not self.cmdline_args.mark_dead:
            return False
        from kython.knetwork import is_alive
        return is_alive(url)
        # TODO should somehow track handle DELETED comments...
        # sometimes it's also [removed]
        # TODO maybe, track that in reddit provider? since we have all version of saved items over time


def setup_parser(p):
    p.add_argument(
        '--mark-dead',
        action='store_true',
        help="Mark deleted/unavailable content so you could process it ASAP. Mostly useful on first run",
    )

if __name__ == '__main__':
    RedditView.main(setup_parser=setup_parser)



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

