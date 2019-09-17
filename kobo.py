#!/usr/bin/env python3
from orger import View
from orger.inorganic import node, link
from orger.org_utils import dt_heading

from my.books.kobo import get_pages, Highlight # type: ignore
# TODO rename to get_books?


class KoboView(View):
    def get_items(self):
        def render_highlight(h: Highlight):
            # TODO FIXME could use bookmark page??
            heading = 'bookmark' if h.kind == 'bookmark' else (h.text or '')
            body = h.annotation # TODO check if empty
            return node(
                heading=dt_heading(h.dt, heading),
                body=body,
            )

        for page in get_pages():
            yield str(page.book), node(
                heading=dt_heading(page.dt, str(page.book)),
                children=[render_highlight(h) for h in page.highlights],
            )


def test():
    from orger.org_utils import pick_heading
    org_tree = KoboView().make_tree()
    ll = pick_heading(org_tree, 'Unsong')
    assert ll is not None
    assert len(ll.children) > 4
    assert any('Singer' in c.render() for c in ll.children)


if __name__ == '__main__':
    KoboView.main()
