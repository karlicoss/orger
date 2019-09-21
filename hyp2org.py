#!/usr/bin/env python3
from orger import InteractiveView
from orger.inorganic import node, link, org_dt
from orger.common import todo

from my.hypothesis import get_todos


class HypTodos(InteractiveView):
    def get_items(self):
        for t in get_todos():
            yield t.eid, todo(
                dt=t.dt,

                heading=t.content,
                tags=['hyp2org', *t.tags],
                body=f'''
{t.annotation}
{link(title=t.title, url=t.link)}
{link(title="in context", url=t.context)}
'''.lstrip(),
            )


if __name__ == '__main__':
    HypTodos.main()
