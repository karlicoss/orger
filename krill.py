#!/usr/bin/env python3
# Automatically import stuff from my Kobo backups into org-mode for further drilling. Mainly using in for learning German words.
# The name stands for K[oboD]rill. Also crustaceans are good for you. 🦐

from typing import Collection

from my.books.kobo import get_highlights, Highlight # type: ignore

from org_view import OrgViewAppend, OrgWithKey
from org_utils import OrgTree, as_org, pick_heading


def is_drill(i: Highlight):
    if i.kind == 'bookmark':
        return
    ann = i.annotation
    if ann is None:
        ann = ''
    if ann.strip().lower() == 'drill':
        return True
    words = i.text.strip().split()
    if len(words) <= 1:
        # might result in a false positive but can just not drill it and remove
        return True
    return False


def get_drill_items():
    return list(sorted(filter(is_drill, get_highlights()), key=lambda h: h.dt))


class Krill(OrgViewAppend):
    file = __file__
    logger_tag = 'krill'

    # pylint: disable=unsubscriptable-object
    def get_items(self) -> Collection[OrgWithKey]:
        return [(
            i.eid, # TODO shit judging by the state.json, looks like it might be flaky
            OrgTree(as_org(
                todo=True,
                inline_created=False,
                heading=i.text,
                body=f'from {i.title}',
                created=i.dt,
                tags=['drill'],
            ))
        ) for i in get_drill_items()]


def main():
    Krill.main(default_to='krill.org', default_state='krill.json')


if __name__ == '__main__':
    main()
