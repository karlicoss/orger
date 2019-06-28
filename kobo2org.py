#!/usr/bin/env python3
from typing import Collection

from my.books.kobo import get_todos, Highlight # type: ignore

from orger.org_view import OrgViewAppend, OrgWithKey
from orger.org_utils import OrgTree, as_org, pick_heading

class KoboTodos(OrgViewAppend):
    file = __file__
    logger_tag = 'kobo-todos'

    # pylint: disable=unsubscriptable-object
    def get_items(self) -> Collection[OrgWithKey]:
        return [(
            t.eid, # TODO shit judging by the state.json, looks like it might be flaky
            OrgTree(as_org(
                todo=True,
                inline_created=False,
                heading=t.text,
                body=f'{t.annotation}\nfrom {t.book}',
                created=t.dt,
                tags=['kobo2org'],
            ))
        ) for t in get_todos()]


# TODO test?
# def test():
#     org_tree = KoboView().make_tree()
#     ll = pick_heading(org_tree, 'Unsong')
#     assert ll is not None
#     assert len(ll.children) > 4
#     assert any('Singer' in c.item for c in ll.children)


def main():
    KoboTodos.main(default_to='kobo2org.org', default_state='kobo2org.json')

if __name__ == '__main__':
    main()
