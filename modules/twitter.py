#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link, timestamp, OrgNode
from orger.common import dt_heading

import datetime
from typing import List

import my.twitter as twi

today = datetime.datetime.now()


class TwitterView(StaticView):
    @property
    def mode(self) -> str:
        assert self.cmdline_args is not None
        return self.cmdline_args.mode

    def _get_tweets(self) -> List[twi.Tweet]:
        if self.mode == 'all':
            return twi.tweets_all()
        else:
            tw = twi.predicate_date(lambda d: d.day == today.day and d.month == today.month) # not gonna work on 29 feb!!
            return tw

    def _render(self, t: twi.Tweet) -> OrgNode:
        dtime = t.dt
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


    def get_items(self):
        for tweet in self._get_tweets():
            yield tweet.tid, self._render(tweet)


def setup_parser(p):
    p.add_argument('--mode', choices=['thatday', 'all'], required=True)


if __name__ == '__main__':
    TwitterView.main(setup_parser=setup_parser)

