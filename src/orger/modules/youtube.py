#!/usr/bin/env python3
from __future__ import annotations

from itertools import groupby

from orger import Mirror
from orger.common import dt_heading, error
from orger.inorganic import link, node


class YoutubeView(Mirror):
    @property
    def mode(self) -> str:
        assert self.cmdline_args is not None
        return self.cmdline_args.mode

    def get_items(self) -> Mirror.Results:
        from my.youtube.takeout import watched

        good = []
        for i in watched():
            if isinstance(i, Exception):
                yield error(i)
            else:
                good.append(i)

        by_when = lambda w: w.when
        if self.mode == 'last':
            by_url = lambda w: w.url
            # fmt: off
            items = [
                max(group, key=by_when)
                for _, group in groupby(sorted(good, key=by_url), key=by_url)
            ]
            # fmt: on
        else:
            items = sorted(good, key=by_when)
        for item in items:
            deleted = item.url == item.title  # todo move to HPI?
            l = link(title=item.title + (' (DELETED)' if deleted else ''), url=item.url)
            yield (item.url, node(heading=dt_heading(item.when, l)))


def setup_parser(p) -> None:
    p.add_argument(
        '--mode', choices=['all', 'last'], default='last', help="'all' would dump all watch history, 'last' only last watch for each video"
    )


if __name__ == '__main__':
    YoutubeView.main(setup_parser=setup_parser)
