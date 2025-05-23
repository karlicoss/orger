#!/usr/bin/env python3
"""
Module for Materialistic app for Hackernews
https://play.google.com/store/apps/details?id=io.github.hidroh.materialistic
"""

from my.hackernews.materialistic import saves

from orger import Queue
from orger.common import dt_heading
from orger.inorganic import link, node


class Materialistic(Queue):
    def get_items(self):
        for s in saves():
            yield (
                s.uid,
                node(
                    heading=dt_heading(
                        dt=s.when,
                        heading=link(title=s.title, url=s.hackernews_link),
                    ),
                    body=s.url,
                ),
            )


if __name__ == '__main__':
    Materialistic.main()
