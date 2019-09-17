#!/usr/bin/env python3
from orger import Interactive
from orger.inorganic import node, link, org_dt

from my.hypothesis import get_todos


class HypTodos(Interactive):
    file = __file__
    logger_tag = 'hypothesis-todos'

    def get_items(self):
        for t in get_todos():
            yield (t.eid, node(
                heading=t.content,
                tags=['hyp2org', *t.tags],

                # TODO could group these three into a helper
                todo='TODO',
                scheduled=t.dt.date(),
                properties={'CREATED': org_dt(t.dt, inactive=True)},

                body=f'''
{t.annotation}
{link(title=t.title, url=t.link)}
{link(title="in context", url=t.context)}
'''.lstrip(),
            ))


def main():
    HypTodos.main(default_to='hyp2org.org', default_state='hyp2org.state')


if __name__ == '__main__':
    main()
