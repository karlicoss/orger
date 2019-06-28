#!/usr/bin/env python3
from typing import Collection

from my.books.kobo import get_pages, Highlight # type: ignore
# TODO rename to get_books?

from orger.org_view import OrgViewOverwrite, OrgWithKey
from orger.org_utils import OrgTree, as_org, pick_heading

class KoboView(OrgViewOverwrite):
    file = __file__
    logger_tag = 'kobo-view'

    # pylint: disable=unsubscriptable-object
    def get_items(self) -> Collection[OrgWithKey]:
        def render_highlight(h: Highlight) -> OrgTree:
            # TODO FIXME could use bookmark page??
            heading = 'bookmark' if h.kind == 'bookmark' else h.text
            body = h.annotation # TODO check if empty
            return OrgTree(as_org(
                created=h.dt,
                heading=heading,
                body=body,
            ))

        return [(
            page.book,
            OrgTree(
                as_org(
                    created=page.dt,
                    heading=str(page.book),
                ),
                [render_highlight(h) for h in page.highlights],
            )
        ) for page in get_pages()]


def test():
    org_tree = KoboView().make_tree()
    ll = pick_heading(org_tree, 'Unsong')
    assert ll is not None
    assert len(ll.children) > 4
    assert any('Singer' in c.item for c in ll.children)


def main():
    KoboView.main(default_to='kobo.org')

if __name__ == '__main__':
    main()
