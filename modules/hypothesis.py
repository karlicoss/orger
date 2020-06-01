#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link
from orger.common import dt_heading, error

import my.hypothesis as hypothesis


class HypView(Mirror):
    def get_items(self) -> Mirror.Results:
        for page in hypothesis.pages():
            # TODO would be nice to signal error upwards? Maybe just yield Exception, rener it in Orger and allow setting error status?
            if isinstance(page, Exception):
                yield error(page)
                continue
            yield node(
                heading=dt_heading(page.created, link(title=page.title, url=page.url)),
                children=[node(
                    heading=dt_heading(hl.created, link(title='context', url=hl.hyp_link)),
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
