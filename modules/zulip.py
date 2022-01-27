#!/usr/bin/env python3

from orger import Mirror
from orger.inorganic import node, link, Quoted
from orger.common import dt_heading, error
from orger import pandoc

from more_itertools import bucket

from my.zulip.organization import messages


class Zulip(Mirror):
    def get_items(self) -> Mirror.Results:
        good = []
        for m in messages():
            if isinstance(m, Exception):
                yield error(m)
                continue
            good.append(m)

        groups = bucket(good, key=lambda m: m.subject)
        for subject in groups:
            group = list(groups[subject])

            def chit():
                for m in group:
                    yield node(
                        heading=dt_heading(m.sent, m.sender),
                        body=pandoc.to_org(m.content, from_='markdown'),
                    )

            yield node(
                heading=dt_heading(group[0].sent, subject), # TODO link
                children=list(chit()),
            )


test = Zulip.make_test(
    heading='Tracking Books',
    contains='progress from my Kobo to Goodreads',
)


if __name__ == '__main__':
    Zulip.main()
