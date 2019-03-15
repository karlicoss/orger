#!/usr/bin/env python3
from typing import NamedTuple, List, Any, Iterable, Tuple, Optional

from my.instapaper import get_pages # type: ignore

from kython.org_tools import link as org_link

from org_view import OrgView
from org_utils import OrgTree, as_org, pick_heading


class IpView(OrgView):
    def get_items(self) -> Iterable[OrgTree]:
        return [
            OrgTree(
                as_org(
                    created=page.bookmark.dt,
                    heading=f'{org_link(title="ip", url=page.bookmark.instapaper_link)}   {org_link(title=page.bookmark.title, url=page.bookmark.url)}',
                ),
                [
                    OrgTree(as_org(
                        created=hl.dt,
                        heading=org_link(title="ip", url=page.bookmark.instapaper_link),
                        body=hl.text,
                    )) for hl in page.highlights
                ]
            ) for page in get_pages()
        # TODO make sure as_org figures out the date
    # TODO autostrip could be an option for formatter
        ]
        # TODO could put links in org mode links? so not as much stuff is displayed?
        # TODO reverse order? not sure...
        # TODO unique id meaning that instapaper manages the item?
        # TODO spacing top level items could be option of dumper as well?
        # TODO better error handling, cooperate with org_tools


# TODO FIXME run ruci against it?
# TODO FIXME careful, sanitize stars somehow.... perhaps replace?
# TODO FIXME need to make sure it's excluded from wereyouhere... otherwise too many duplications and unncessary links?
# TODO hmm. wereyouhere could explore automatically, perhaps even via porg?
# make it a feature of renderer?
# although just need to make one space tabulation, that'd solve all my problems
def test():
    org_tree = IpView(
        logger_tag='instapaper-view',
        default_to='instapaper.org',
        file_header='dummy',
    ).make_tree()
    ll = pick_heading(org_tree, 'Life Extension Methods')
    assert ll is not None
    assert len(ll.children) > 4
    assert any('sleep a lot' in c.item for c in ll.children)


def main():
    IpView(
        logger_tag='instapaper-view',
        default_to='instapaper.org',
        file_header=f"# AUTOGENERATED BY {__file__}\n", # TODO date?
    ).main()

if __name__ == '__main__':
    main()