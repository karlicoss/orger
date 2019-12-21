#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading, error

from my.hypothesis import get_pages


class HypView(StaticView):
    def get_items(self):
        for page in get_pages():
            # TODO would be nice to signal error upwards? Maybe just yield Exception, rener it in Orger and allow setting error status?
            if isinstance(page, Exception):
                yield error(page)
                continue
            yield node(
                heading=dt_heading(page.dt, link(title=page.title, url=page.link)),
                children=[node(
                    heading=dt_heading(hl.dt, link(title='context', url=hl.hyp_link)),
                    tags=hl.tags,
                    body=hl.highlight,
                    children=[] if hl.annotation is None else [node(
                        heading=hl.annotation,
                    )]
                ) for hl in page.highlights]
            )


# TODO tests for determinism
# TODO they could also be extracted to common routine and used in each provider
# TODO need to group by source??

if __name__ == '__main__':
    HypView.main()
