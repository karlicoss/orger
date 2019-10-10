#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading

from my.media.youtube import get_watched

from itertools import groupby

class YoutubeView(StaticView):
    def get_items(self):
        watched = get_watched()
        by_url  = lambda w: w.url
        by_when = lambda w: w.when
        items = [
            max(group, key=by_when)
            for _, group in groupby(sorted(watched, key=by_url), key=by_url)
        ]
        items = sorted(items, key=by_when)
        # TODO for each url only take latest?
        for item in items:
            yield (item.url, node(
                heading=dt_heading(item.when, link(title=item.title, url=item.url)),
            ))


if __name__ == '__main__':
    YoutubeView.main()
