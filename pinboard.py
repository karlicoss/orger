#!/usr/bin/env python3
from typing import NamedTuple, List, Any, Iterable, Tuple, Optional, Collection

from kython.kerror import unwrap
from kython.org_tools import link as org_link

from org_view import OrgViewOverwrite, OrgWithKey
from org_utils import OrgTree, as_org, pick_heading

from my.bookmarks import pinboard

class PinboardView(OrgViewOverwrite):
    file = __file__
    logger_tag='pinboard-view'

    # pylint: disable=unsubscriptable-object
    def get_items(self) -> Collection[OrgWithKey]:
        def make_item(res: pinboard.Result) -> OrgWithKey:
            try:
                b = unwrap(res)
            except pinboard.Error as e:
                return f'error_{e.uid}', OrgTree(as_org(heading=str(e)))
            else:
                return b.uid, OrgTree(as_org(
                    created=b.created,
                    heading=org_link(title=b.title, url=b.url),
                    body=b.description,
                    tags=b.tags,
                ))
        return [make_item(b) for b in pinboard.get_entries()]

def test():
    tree = PinboardView().make_tree()
    ll = pick_heading(tree, 'Cartesian Closed Comic #21')
    assert ll is not None
    assert 'doctorwho' in ll.item


def main():
    PinboardView.main(default_to='pinboard.org')


if __name__ == '__main__':
    main()



