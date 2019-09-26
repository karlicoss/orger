#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading

from my.hypothesis import get_pages


class HypView(StaticView):
    def get_items(self):
        for page in get_pages():
            yield node(
                heading=dt_heading(page.dt, link(title=page.title, url=page.link)),
                children=[node(
                    heading=dt_heading(hl.dt, link(title='context', url=hl.hyp_link)),
                    tags=hl.tags,
                    body=hl.content,
                    children=[] if hl.text is None else [node(
                        heading=hl.text,
                    )]
                ) for hl in page.annotations]
            )


# TODO tests for determinism
# TODO they could also be extracted to common routine and used in each provider
# TODO need to group by source??

if __name__ == '__main__':
    HypView.main()
