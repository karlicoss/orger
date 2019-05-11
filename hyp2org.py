#!/usr/bin/env python3
from typing import Collection

from my.hypothesis import get_todos # type: ignore

from kython.org_tools import link as org_link

from org_view import OrgViewAppend, OrgWithKey
from org_utils import OrgTree, as_org


class HypTodos(OrgViewAppend):
    file = __file__
    logger_tag = 'hypothesis-todos'

    # pylint: disable=unsubscriptable-object
    def get_items(self) -> Collection[OrgWithKey]:
        return [(
            t.eid,
            OrgTree(as_org(
                todo=True,
                inline_created=False,
                heading=t.content,
                body=f'''
{t.annotation}
{org_link(title=t.title, url=t.link)}
{org_link(title="in context", url=t.context)}
'''.strip(),
                created=t.dt,
                tags=['hyp2org', *t.tags],
            ))
        ) for t in get_todos()]


def main():
    HypTodos.main(default_to='hyp2org.org', default_state='hyp2org.state')

if __name__ == '__main__':
    main()
