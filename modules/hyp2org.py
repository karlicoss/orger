#!/usr/bin/env python3
from orger import InteractiveView
from orger.inorganic import node, link
from orger.common import todo

from my.hypothesis import get_highlights, Annotation


def is_todo(e: Annotation) -> bool:
    if any(t.lower() == 'todo' for t in e.tags):
        return True
    text = e.text or ''
    return text.lstrip().lower().startswith('todo')


class HypTodos(InteractiveView):
    def get_items(self):
        for t in filter(is_todo, get_highlights()):
            yield t.eid, todo(
                dt=t.dt,

                heading=t.content,
                tags=['hyp2org', *t.tags],
                body=f'''
{t.text}
{link(title=t.title, url=t.link)}
{link(title="in context", url=t.context)}
'''.lstrip(),
            )


if __name__ == '__main__':
    HypTodos.main()
