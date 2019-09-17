#!/usr/bin/env python3
from my.hypothesis import get_pages

from kython.org_tools import link as org_link

from orger.org_view import OrgViewOverwrite, OrgWithKey
from orger.org_utils import OrgTree, as_org, OrgNode


from orger.inorganic import datetime2org

def node(**kwargs):
    return OrgNode(**kwargs)

from datetime import datetime
def dt_heading(dt: datetime, heading: str):
    """
    Helper to inline datetime in heading
    """
    # TODO move to inorganic? not sure
    return '[{}] '.format(datetime2org(dt)) + heading


class HypView(OrgViewOverwrite):
    file = __file__
    logger_tag = 'hypothesis-view'

    def get_items(self):
        # TODO FIXME overwrite doesn't need pairs?
        for page in get_pages():
            yield (page.link, node(
                # TODO FIXME inline created?
                heading=dt_heading(page.dt, org_link(title=page.title, url=page.link)),
                children=[node(
                    heading=dt_heading(hl.dt, org_link(title='context', url=hl.hyp_link)),
                    tags=hl.tags,
                    body=hl.content,
                    children=[] if hl.annotation is None else [node(
                        heading=hl.annotation,
                    )]
                ) for hl in page.highlights]
            ))

    def get_items_old(self):
        for page in get_pages():
            yield (page.link, OrgTree(
                [
                    OrgTree(as_org(
                        created=hl.dt,
                        heading=org_link(title='context', url=hl.hyp_link),
                        body=hl.content,
                        tags=hl.tags,
                    ), [] if hl.annotation is None else [OrgTree(as_org(body=hl.annotation))]) for hl in page.highlights
                ]
            ))


# TODO tests for determinism
# TODO they could also be extracted to common routine and used in each provider

def main():
    # TODO default_to could depend on filename?
    HypView.main(default_to='hypothesis.org')
    # TODO need to group by source??

if __name__ == '__main__':
    main()
