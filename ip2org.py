#!/usr/bin/env python3
from typing import Collection

from kython.org_tools import link as org_link

from org_view import OrgViewAppend, OrgWithKey
from org_utils import OrgTree, as_org, pick_heading

from my.instapaper import get_todos # type: ignore

class IpTodos(OrgViewAppend):
    file = __file__
    logger_tag = 'instapaper-todos'

    # pylint: disable=unsubscriptable-object
    def get_items(self) -> Collection[OrgWithKey]:
        return [(
            t.uid,
            OrgTree(as_org(
                todo=True,
                inline_created=False,
                heading=t.text,
                body=f'{t.note}\nfrom {org_link(title="ip", url=t.instapaper_link)}   {org_link(title=t.title, url=t.url)}',
                # TODO scheduled!, looks like it's automatic if todo=True? kinda makes sens
                created=t.dt,
                tags=['ip2org'],
            ))
        ) for t in get_todos()]


# TODO add some test
# def test():
#     org_tree = IpView().make_tree()
#     ll = pick_heading(org_tree, 'Life Extension Methods')
#     assert ll is not None
#     assert len(ll.children) > 4
#     assert any('sleep a lot' in c.item for c in ll.children)


def main():
    IpTodos.main(default_to='ip2org.org', default_state='ip2org.json')

if __name__ == '__main__':
    main()
