#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link
from orger.common import dt_heading

from my.media.youtube import watched

from itertools import groupby


class YoutubeView(Mirror):
    def get_items(self) -> Mirror.Results:
        by_url  = lambda w: w.url
        by_when = lambda w: w.when
        items = [
            max(group, key=by_when)
            for _, group in groupby(sorted(watched(), key=by_url), key=by_url)
        ]
        items = sorted(items, key=by_when)
        # TODO for each url only take latest?
        for item in items:
            deleted = item.url == item.title # todo move to HPI?
            l = link(title=item.title + (' (DELETED)' if deleted else ''), url=item.url)
            yield (item.url, node(
                heading=dt_heading(item.when, l),
            ))


if __name__ == '__main__':
    YoutubeView.main()
