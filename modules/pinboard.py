#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link
from orger.common import dt_heading

import my.pinboard as pinboard


class PinboardView(Mirror):
    def get_items(self) -> Mirror.Results:
        from orger.inorganic import OrgNode
        def make_item(b: pinboard.Bookmark) -> OrgNode:
            return node(
                heading=dt_heading(b.created, link(title=b.title, url=b.url)),
                body=b.description,
                tags=b.tags,
            )
        return [make_item(b) for b in pinboard.bookmarks()]


test = PinboardView.make_test(
    heading='Cartesian Closed Comic #21',
    contains='doctorwho', # todo predicate?
)

if __name__ == '__main__':
    PinboardView.main()


# todo need to use hpi module install my.pinbpoar
