#!/usr/bin/env python3
from orger import View
from orger.inorganic import node, link
from orger.org_utils import dt_heading

from my.hypothesis import get_pages


class HypView(View):
    def get_items(self):
        # TODO FIXME View doesn't need pairs?
        for page in get_pages():
            yield (page.link, node(
                heading=dt_heading(page.dt, link(title=page.title, url=page.link)),
                children=[node(
                    heading=dt_heading(hl.dt, link(title='context', url=hl.hyp_link)),
                    tags=hl.tags,
                    body=hl.content,
                    children=[] if hl.annotation is None else [node(
                        heading=hl.annotation,
                    )]
                ) for hl in page.highlights]
            ))


# TODO tests for determinism
# TODO they could also be extracted to common routine and used in each provider
# TODO need to group by source??

if __name__ == '__main__':
    HypView.main()
