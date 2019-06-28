#!/usr/bin/env python3
from typing import NamedTuple, List, Any, Iterable, Tuple, Optional, Collection

from kython.org import datetime2org
from kython.org_tools import link as org_link
from kython import parse_date_new
today = parse_date_new('today')

from orger.org_view import OrgViewOverwrite, OrgWithKey
from orger.org_utils import OrgTree, as_org, pick_heading

import my.tweets

class TwitterView(OrgViewOverwrite):
    file = __file__
    logger_tag = 'twitter-view'

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

    def _render(self, t: my.tweets.Tweet) -> OrgTree:
        dtime = t.dt
        text = t.text
        url = t.url
        link = org_link(title=text, url=url)
        if self.mode == 'all':
            return OrgTree(as_org(
                created=dtime,
                heading=link,
                tags=['tweet'],
            ))
        else:
            dd = dtime.replace(year=today.year)
            return OrgTree(as_org(
                # TODO instead wrap in something like active and passive
                created=dd.date(),
                active_created=True,

                heading=f"at [{datetime2org(dtime)}] {link}",
                tags=['ttweet'],
            ))


    # pylint: disable=unsubscriptable-object
    def get_items(self) -> Collection[OrgWithKey]:
        return [(
            tweet.tid,
            self._render(tweet),
        ) for tweet in self._get_tweets()]


def setup_parser(p):
    p.add_argument('--mode', choices=['thatday', 'all'], required=True)


def main():
    TwitterView.main(default_to='ttweets.org', setup_parser=setup_parser)


if __name__ == '__main__':
    main()

