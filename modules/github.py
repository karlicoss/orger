#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading

import my.coding.github as gh


class Github(StaticView):
    def get_items(self):
        for e in gh.get_events():
            # TODO filter only events that have body? e.g. not sure if much point emitting pull requests here
            yield node(
                dt_heading(
                    e.dt,
                    link(url=e.link, title=e.summary) if e.link is not None else e.summary
                ),
                # TODO would be nice to convert from markdown to org here
                body=e.body,
            )


if __name__ == '__main__':
    Github.main()
