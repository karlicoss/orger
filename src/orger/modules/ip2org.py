#!/usr/bin/env python3
from my.instapaper import is_todo, pages

from orger import Queue
from orger.common import todo
from orger.inorganic import link


class IpTodos(Queue):
    def get_items(self) -> Queue.Results:
        for page in pages():
            bm = page.bookmark
            for hl in page.highlights:
                if not is_todo(hl):
                    continue
                yield (
                    hl.hid,
                    todo(
                        # todo dt_heading? not sure. Maybe this should be configurable
                        dt=hl.dt,
                        heading=link(title="X", url=hl.instapaper_link) + ' ' + hl.text,
                        tags=['ip2org'],
                        body=f'{hl.note}\nfrom {link(title=bm.title, url=bm.url)}',
                    ),
                )


if __name__ == '__main__':
    IpTodos.main()


# TODO move error handling to the base class
# TODO add some test?
