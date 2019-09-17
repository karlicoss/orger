#!/usr/bin/env python3
from orger import View
from orger.inorganic import node, link
from orger.org_utils import dt_heading

from my.media.youtube import get_watched

from kython import group_by_key

class YoutubeView(View):
    def get_items(self):
        watched = get_watched()
        items = [
            max(group, key=lambda w: w.when)
            for _, group in group_by_key(watched, key=lambda w: w.url).items()
        ]
        items = sorted(items, key=lambda w: w.when)
        # TODO for each url only take latest?
        for item in items:
            yield (item.url, node(
                heading=dt_heading(item.when, link(title=item.title, url=item.url)),
            ))


if __name__ == '__main__':
    YoutubeView.main()
