#!/usr/bin/env python3
"""
Sometimes when I'm annotating using [[https://hypothes.is][Hypothesis]], I want to think more
about specific highlights, google more about them later or generally act on them somehow.

Normally you'd have to copy the URL, highlighted text and create a task from it.

This script does that automatically, only thing that you have to do is to mark it with a tag or type 'todo'
in the annotation text.

Items get scheduled and appear on my org-mode agenda,
so I can un/reschedule them if they don't require immediate attention.
"""

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
