#!/usr/bin/env python3
from orger import StaticView, OrgWithKey
from orger.inorganic import node, link
from orger.common import dt_heading

from kython.kerror import unwrap

from my.reading import polar

class PolarView(StaticView):
    def get_items(self):
        def make_item(res: polar.Result) -> OrgWithKey:
            try:
                b = unwrap(res)
            except polar.Error as e:
                return f'error_{e.uid}', node(heading=str(e))
            else:
                return b.uid, node(
                    heading=dt_heading(b.created, f'{b.title} {b.filename}'),
                    # tags=b.tags, # TODO?
                    children=[node(
                        heading=dt_heading(hl.created, hl.selection),
                        # TODO some shitty characters; generally concatenated text doesn't look great...
                        children=[node(
                            heading=dt_heading(c.created, c.text)
                        ) for c in hl.comments]
                    ) for hl in b.items]
                )
        for b in polar.get_entries():
            yield make_item(b)


test = PolarView.make_test(
    heading='I missed the bit where he only restricted to spin'
)


if __name__ == '__main__':
    PolarView.main()

