#!/usr/bin/env python3
# TODO add tags?
from my.pocket import articles

from orger import Mirror
from orger.common import dt_heading
from orger.inorganic import link, node


class PocketMirror(Mirror):
    def get_items(self) -> Mirror.Results:
        for a in articles():
            yield node(
                heading=dt_heading(
                    a.added,
                    link(title='pocket', url=a.pocket_link)  + ' · ' + link(title=a.title, url=a.url)
                ),
                children=[node(
                    heading=dt_heading(hl.created, hl.text)
                ) for hl in a.highlights]
            )


if __name__ == '__main__':
    PocketMirror.main()
