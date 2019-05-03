#!/usr/bin/env python3
from typing import NamedTuple, List, Any, Iterable, Tuple, Optional, Collection

from kython.kerror import unwrap
from kython.org_tools import link as org_link

from org_view import OrgViewOverwrite, OrgWithKey
from org_utils import OrgTree, as_org, pick_heading

from my.reading import polar

class PolarView(OrgViewOverwrite):
    file = __file__
    logger_tag = 'polar-view'

    # pylint: disable=unsubscriptable-object
    def get_items(self) -> Collection[OrgWithKey]:
        def make_item(res: polar.Result) -> OrgWithKey:
            try:
                b = unwrap(res)
            except polar.Error as e:
                return f'error_{e.uid}', OrgTree(as_org(heading=str(e)))
            else:
                return b.uid, OrgTree(as_org(
                    created=b.created,
                    # TODO what's in body??
                    heading=f'{b.title} {b.filename}',
                    # body=b.description, 
                    # tags=b.tags,
                ))
        return [make_item(b) for b in polar.get_entries()]

def test():
    # TODO FIXME
    tree = PinboardView().make_tree()
    ll = pick_heading(tree, 'Cartesian Closed Comic #21')
    assert ll is not None
    assert 'doctorwho' in ll.item


def main():
    PolarView.main(default_to='polar.org')


if __name__ == '__main__':
    main()



