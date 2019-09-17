#!/usr/bin/env python3
from orger import Interactive
from orger.inorganic import node, link
from orger.org_utils import dt_heading

from my.hypothesis import get_todos

from kython.org_tools import link as org_link

from orger import OrgViewAppend, OrgWithKey
from orger.org_utils import OrgTree, as_org


class HypTodos(Interactive):
    file = __file__
    logger_tag = 'hypothesis-todos'

    def get_items(self):
        for t in get_todos():
            yield (t.eid, node(
                heading=t.content,
                todo='TODO',
                # TODO created property?
                inline_created=False,
                body=f'''
{t.annotation}
{org_link(title=t.title, url=t.link)}
{org_link(title="in context", url=t.context)}
'''.strip(),
                created=t.dt,
                tags=['hyp2org', *t.tags],
            ))
        )


def main():
    HypTodos.main(default_to='hyp2org.org', default_state='hyp2org.state')


if __name__ == '__main__':
    main()
