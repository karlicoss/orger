#!/usr/bin/env python3
from typing import NamedTuple, List, Any, Iterable, Tuple, Optional, Collection

from my.hypothesis import get_pages # type: ignore

from kython.org_tools import link as org_link

from org_view import OrgViewOverwrite, OrgWithKey
from org_utils import OrgTree, as_org


class HypView(OrgViewOverwrite):
    file = __file__
    logger_tag = 'hypothesis-view'

    # pylint: disable=unsubscriptable-object
    def get_items(self) -> Collection[OrgWithKey]:
        return [(
            page.link,
            OrgTree(
                as_org(
                    created=page.dt,
                    heading=org_link(title=page.title, url=page.link),
                ),
                [
                    OrgTree(as_org(
                        created=hl.dt,
                        heading=org_link(title='hyp', url=hl.hyp_link),
                        body=hl.content, # TODO annotation??
                    )) for hl in page.highlights
                ]
            )
        ) for page in get_pages()]


# TODO tests for determinism

def main():
    HypView.main(default_to='hypothesis.org')
    # TODO need to group by source??

if __name__ == '__main__':
    main()
