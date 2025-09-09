#!/usr/bin/env python3
import datetime
from collections.abc import Iterable

# shit... this is annoying, need to 'nudge' the config so it picks up all.py override?
import my.twitter.all as twi
from my.core import Res

from orger import Mirror
from orger.common import dt_heading, error
from orger.inorganic import OrgNode, link, node, timestamp

today = datetime.datetime.now()

Tweet = twi.Tweet


class TwitterView(Mirror):
    @property
    def mode(self) -> str:
        assert self.cmdline_args is not None
        return self.cmdline_args.mode

    def _get_tweets(self) -> Iterable[Res[Tweet]]:
        if self.mode == 'all':
            return twi.tweets()
        else:
            # not gonna work on 29 feb!!
            same_day = lambda d: d.day == today.day and d.month == today.month
            return (t for t in twi.tweets() if isinstance(t, Exception) or same_day(t.created_at))

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
            text = '  ' + text if text.startswith('@') else text  # pad replies a bit
            heading = (
                timestamp(dd.date(), active=True)
                + ' '
                + f"{link(title='TW', url=url)} at {timestamp(dtime, inactive=True)} {text}"
            )
            return node(
                heading=heading,
                tags=['ttweet'],
            )

    def get_items(self) -> Mirror.Results:
        good = []
        for t in self._get_tweets():
            if isinstance(t, Exception):
                yield error(t)
            else:
                good.append(t)

        for tweet in sorted(good, key=lambda t: t.created_at):
            yield self._render(tweet)


def setup_parser(p) -> None:
    p.add_argument('--mode', choices=['thatday', 'all'], required=True)


if __name__ == '__main__':
    TwitterView.main(setup_parser=setup_parser)
