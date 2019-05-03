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
                    heading=f'{b.title} {b.filename}',
                    # tags=b.tags, # TODO?
                ), [
                    OrgTree(as_org(
                        created=hl.created,
                        heading=hl.selection, # TODO some shitty characters; generally concatenated text doesn't look great...
                    ), [
                        OrgTree(as_org(
                            created=c.created,
                            heading=c.text,
                        )) for c in hl.comments
                    ]) for hl in b.items
                ])
        return [make_item(b) for b in polar.get_entries()]

def test():
    tree = PolarView().make_tree()
    ll = pick_heading(tree, 'I missed the bit where he only restricted to spin')
    assert ll is not None
    # TODO more tests?


def main():
    PolarView.main(default_to='polar.org')


if __name__ == '__main__':
    main()



