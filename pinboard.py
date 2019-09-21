#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading
from orger.org_view import OrgWithKey

from kython.kerror import unwrap
# TODO rename unwrap to make it more consistent with rust?

from my.bookmarks import pinboard

class PinboardView(StaticView):
    def get_items(self):
        def make_item(res: pinboard.Result) -> OrgWithKey:
            try:
                b = unwrap(res)
            except pinboard.Error as e:
                return f'error_{e.uid}', node(heading=str(e))
            else:
                return b.uid, node(
                    heading=dt_heading(b.created, link(title=b.title, url=b.url)),
                    body=b.description,
                    tags=b.tags,
                )
        return [make_item(b) for b in pinboard.get_entries()]


test = PinboardView.make_test(
    heading='Cartesian Closed Comic #21',
    contains='doctorwho', # TODO predicate?
)

if __name__ == '__main__':
    PinboardView.main()

