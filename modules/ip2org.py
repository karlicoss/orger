#!/usr/bin/env python3
from orger import InteractiveView
from orger.inorganic import node, link
from orger.common import todo

from my.instapaper import get_todos # type: ignore


class IpTodos(InteractiveView):
    def get_items(self):
        for t in get_todos():
            # TODO move erorr handling to base renderer?
            hl = t.highlight
            bm = t.bookmark
            yield hl.hid, todo(
                dt=hl.dt,

                heading=hl.text,
                tags=['ip2org'],
                body=f'{hl.note}\nfrom {link(title="ip", url=hl.instapaper_link)}   {link(title=bm.title, url=bm.url)}',
            )

# TODO add some test?


if __name__ == '__main__':
    IpTodos.main()
