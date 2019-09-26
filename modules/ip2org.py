#!/usr/bin/env python3
from orger import InteractiveView
from orger.inorganic import node, link
from orger.common import todo

from my.instapaper import get_todos # type: ignore


class IpTodos(InteractiveView):
    def get_items(self):
        for t in get_todos():
            # TODO move erorr handling to base renderer?
            yield t.uid, todo(
                dt=t.dt,

                heading=t.text,
                tags=['ip2org'],
                body=f'{t.note}\nfrom {link(title="ip", url=t.instapaper_link)}   {link(title=t.title, url=t.url)}',
            )

# TODO add some test?


if __name__ == '__main__':
    IpTodos.main()
