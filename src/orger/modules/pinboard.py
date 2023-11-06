#!/usr/bin/env python3
from typing import List

from orger import Mirror
from orger.common import dt_heading, error
from orger.inorganic import node, link

import my.pinboard as pinboard


class PinboardView(Mirror):
    def get_items(self) -> Mirror.Results:
        items: List[pinboard.Bookmark] = []
        for b in pinboard.bookmarks():
            if isinstance(b, Exception):
                yield error(b)
            else:
                items.append(b)

        for b in sorted(
            items,
            # need to sort by some other property since all initial exports have the same timestamp
            # doesn't look like there is any sort of bookmark id for pinboard
            key=lambda b: (b.created, b.url),
        ):
            yield node(
                heading=dt_heading(b.created, link(title=b.title, url=b.url)),
                body=b.description,
                tags=b.tags,
            )


test = PinboardView.make_test(
    heading='Cartesian Closed Comic #21',
    contains='doctorwho',  # todo predicate?
)

if __name__ == '__main__':
    PinboardView.main()


# todo need to use hpi module install my.pinbpoar
