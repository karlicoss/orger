#!/usr/bin/env python3
"""
Module for Materialistic app for Hackernews
https://play.google.com/store/apps/details?id=io.github.hidroh.materialistic
"""

from orger import InteractiveView
from orger.inorganic import node, link
from orger.common import dt_heading

from my.materialistic import saves

class MaterialisticView(InteractiveView):
    def get_items(self):
        for s in saves():
            yield s.uid, node(
                heading=dt_heading(
                    s.when,
                    link(title=s.title, url=s.hackernews_link),
                ),
                body=s.url,
            )


if __name__ == '__main__':
    MaterialisticView.main()
