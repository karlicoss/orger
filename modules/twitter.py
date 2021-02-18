#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link, timestamp, OrgNode
from orger.common import dt_heading

import datetime
from typing import Iterable, Any

import my.twitter.all as twi

today = datetime.datetime.now()

# TODO FIXME expose Tweet type in twitter.common module?
Tweet = Any

class TwitterView(Mirror):
    @property
    def mode(self) -> str:
        assert self.cmdline_args is not None
        return self.cmdline_args.mode

    def _get_tweets(self) -> Iterable[Tweet]:
        if self.mode == 'all':
            return twi.tweets()
        else:
            # not gonna work on 29 feb!!
            same_day = lambda d: d.day == today.day and d.month == today.month
            return (t for t in twi.tweets() if same_day(t.created_at))

    def _render(self, t: Tweet) -> OrgNode:
        dtime = t.created_at
        text = t.text
        url = t.permalink
        if self.mode == 'all':
            return node(
                heading=dt_heading(dtime, link(title=text, url=url)),
                tags=['tweet'],
            )
        else:
            dd = dtime.replace(year=today.year)
            text = '  ' + text if text.startswith('@') else text # pad replies a bit
            return node(
                heading=timestamp(dd.date(), active=True) + ' ' + f"{link(title='TW', url=url)} at {timestamp(dtime, inactive=True)} {text}",
                tags=['ttweet'],
            )


    def get_items(self) -> Mirror.Results:
        for tweet in sorted(self._get_tweets(), key=lambda t: t.created_at):
            yield self._render(tweet)


def setup_parser(p) -> None:
    p.add_argument('--mode', choices=['thatday', 'all'], required=True)


if __name__ == '__main__':
    TwitterView.main(setup_parser=setup_parser)

