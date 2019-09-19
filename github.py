#!/usr/bin/env python3
from orger import View
from orger.inorganic import node, link
from orger.org_utils import dt_heading

import my.github as gh


class Github(View):
    def get_items(self):
        for e in gh.get_events():
            # TODO filter only events that have body? e.g. not sure if much point emitting pull requests here
            yield node(
                dt_heading(e.dt, e.summary), # TODO link?
                # TODO body
            )


if __name__ == '__main__':
    Github.main()
