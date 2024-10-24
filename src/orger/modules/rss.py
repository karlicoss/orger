#!/usr/bin/env python3
import my.rss.all as rss

from orger import Mirror
from orger.inorganic import link, node


class RssSubscriptions(Mirror):
    def get_items(self):
        for s in rss.subscriptions():
            yield node(
                link(url=s.url, title=s.title) + ('' if s.subscribed else ' UNSUBSCRIBED'),
            )


if __name__ == '__main__':
    RssSubscriptions.main()
