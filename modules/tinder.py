#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node
from orger.common import dt_heading, error


import my.config
# todo later, use .all?
import my.tinder.android as tinder  # type: ignore[import] # uncomment once we release newer hpi

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

        for match, messages in sorted(res.items(), key=lambda p: p[0].when):
            yield node(
                dt_heading(match.when, match.person.name),
                children=[node(
                    dt_heading(m.sent, f'{m.from_.name}: {m.text}'),
                ) for m in messages]
            )



if __name__ == '__main__':
    TinderView.main()
