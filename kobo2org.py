#!/usr/bin/env python3
from orger import InteractiveView
from orger.inorganic import node, link, org_dt
from orger.common import todo

from my.books.kobo import get_todos, Highlight # type: ignore


class KoboTodos(InteractiveView):
    def get_items(self):
        for t in get_todos():
            # TODO shit judging by the state.json, looks like eid might be flaky?
            yield t.eid, todo(
                t.dt,

                heading=t.text,
                tags=['kobo2org'],
                body=f'{t.annotation}\nfrom {t.book}\n',
            )

# TODO test?

if __name__ == '__main__':
    KoboTodos.main()
