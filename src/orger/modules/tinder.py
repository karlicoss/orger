#!/usr/bin/env python3

# todo later, use .all?
import my.tinder.android as tinder

from orger import Mirror
from orger.common import dt_heading, error
from orger.inorganic import node


class TinderView(Mirror):
    def get_items(self) -> Mirror.Results:
        res = None
        for i in tinder.match2messages():
            assert res is None, res
            if isinstance(i, Exception):
                yield error(i)
            else:
                res = i
        assert res is not None

        for match_, messages in sorted(res.items(), key=lambda p: p[0].when):
            # fmt: off
            yield node(
                dt_heading(
                    dt=match_.when,
                    heading=match_.person.name,
                ),
                children=[
                    node(dt_heading(
                        dt=m.sent,
                        heading=f'{m.from_.name}: {m.text}',
                    ))
                    for m in messages
                ],
            )
            # fmt: on


if __name__ == '__main__':
    TinderView.main()
