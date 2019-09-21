#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link, org_dt, OrgNode
from orger.org_utils import dt_heading

from typing import List

import my.tweets

from kython import parse_date_new
today = parse_date_new('today') # TODO get rid of it...


class TwitterView(StaticView):
    @property
    def mode(self) -> str:
        assert self.cmdline_args is not None
        return self.cmdline_args.mode

    def _get_tweets(self) -> List[my.tweets.Tweet]:
        if self.mode == 'all':
            return my.tweets.tweets_all()
        else:
            tw = my.tweets.predicate_date(lambda d: d.day == today.day and d.month == today.month) # not gonna work on 29 feb!!
            return tw

    def _render(self, t: my.tweets.Tweet) -> OrgNode:
        dtime = t.dt
        text = t.text
        url = t.url
        if self.mode == 'all':
            return node(
                heading=dt_heading(dtime, link(title=text, url=url)),
                tags=['tweet'],
            )
        else:
            dd = dtime.replace(year=today.year)
            text = '  ' + text if text.startswith('@') else text # pad replies a bit
            return node(
                heading=org_dt(dd.date(), active=True) + ' ' + f"{link(title='TW', url=url)} at {org_dt(dtime, inactive=True)} {text}",
                tags=['ttweet'],
            )


    def get_items(self):
        for tweet in self._get_tweets():
            yield tweet.tid, self._render(tweet)


def setup_parser(p):
    p.add_argument('--mode', choices=['thatday', 'all'], required=True)


if __name__ == '__main__':
    TwitterView.main(setup_parser=setup_parser)

