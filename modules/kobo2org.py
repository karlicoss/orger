#!/usr/bin/env python3
from orger import Queue
from orger.inorganic import node, link
from orger.common import todo

from my.books.kobo import get_todos, Highlight


class KoboTodos(Queue):
    def get_items(self) -> Queue.Results:
        for t in get_todos():
            # TODO shit judging by the state.json, looks like eid might be flaky?
            yield t.eid, todo(
                t.dt,

                heading=t.text,
                tags=['kobo2org'], # todo allow to override tag from cmdline?
                body=f'{t.annotation}\nfrom {t.book}\n',
            )

# TODO test?

if __name__ == '__main__':
    KoboTodos.main()


# TODO whould be possible to write modules without classes -- just a single function...
# unclear how to determine result type properly...
