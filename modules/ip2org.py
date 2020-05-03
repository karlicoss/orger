#!/usr/bin/env python3
from orger import InteractiveView
from orger.inorganic import node, link
from orger.common import todo

from my.instapaper import pages, is_todo


class IpTodos(InteractiveView):
    def get_items(self):
        for page in pages():
            bm = page.bookmark
            for hl in page.highlights:
                if not is_todo(hl):
                    continue
                yield hl.hid, todo(
                    dt=hl.dt,
                    heading=hl.text,
                    tags=['ip2org'],
                    body=f'{hl.note}\nfrom {link(title="x", url=hl.instapaper_link)}   {link(title=bm.title, url=bm.url)}',
                )

if __name__ == '__main__':
    IpTodos.main()


# TODO move error handling to the base class
# TODO add some test?
