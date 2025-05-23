#!/usr/bin/env python3
from my.kobo import Highlight, get_books_with_highlights

from orger import Mirror
from orger.common import dt_heading
from orger.inorganic import OrgNode, node


class KoboView(Mirror):
    def get_items(self) -> Mirror.Results:
        def render_highlight(h: Highlight) -> OrgNode:
            # TODO FIXME could use bookmark page??
            heading = 'bookmark' if h.kind == 'bookmark' else (h.text or '')
            body = h.annotation  # TODO check if empty
            return node(
                heading=dt_heading(h.dt, heading),
                body=body,
            )

        for page in get_books_with_highlights():
            yield (
                str(page.book),
                node(
                    heading=dt_heading(page.dt, str(page.book)),
                    children=[render_highlight(h) for h in page.highlights],
                ),
            )


# TODO maybe fixture instead?
test = KoboView.make_test(
    heading='Unsong',
    contains='Singer',
)


if __name__ == '__main__':
    KoboView.main()
