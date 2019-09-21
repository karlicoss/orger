#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.org_utils import dt_heading
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


# TODO FIXME could make test generic perhaps? so you'd only have to specify expected content
def test():
    from orger.org_utils import pick_heading
    tree = PinboardView().make_tree()
    ll = pick_heading(tree, 'Cartesian Closed Comic #21')
    assert ll is not None
    assert 'doctorwho' in ll.render()


if __name__ == '__main__':
    PinboardView.main()

