#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link, Quoted
from orger.common import dt_heading

from my.instapaper import pages


class Instapaper(Mirror):
    def get_items(self) -> Mirror.Results:
        for page in pages():
            yield node(
                heading=dt_heading(
                    page.dt,
                    f'{link(title="x", url=page.bookmark.instapaper_link)}   {link(title=page.title, url=page.url)}',
                ),
                children=[node(
                    heading=dt_heading(hl.dt, link(title="x", url=page.bookmark.instapaper_link)),
                    body=Quoted(hl.text),
                    children=[] if hl.note is None else [
                        node(heading=hl.note),
                    ],
                ) for hl in page.highlights]
            )
        # TODO autostrip could be an option for formatter
        # TODO reverse order? not sure...
        # TODO spacing top level items could be option of dumper as well?
        # TODO better error handling, cooperate with org_tools

# todo move tests to separate files, otherwise they would annoy other people
test = Instapaper.make_test(
    heading='Life Extension Methods',
    contains='sleep a lot',
)


if __name__ == '__main__':
    Instapaper.main()
