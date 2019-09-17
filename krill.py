#!/usr/bin/env python3
# Automatically import stuff from my Kobo backups into org-mode for further drilling. Mainly using in for learning German words.
# The name stands for K[oboD]rill. Also crustaceans are good for you. 🦐
from orger import Interactive
from orger.inorganic import node, link, org_dt
from orger.org_utils import todo

from my.books.kobo import get_highlights, Highlight # type: ignore

def is_drill(i: Highlight):
    if i.kind == 'bookmark':
        return
    ann = i.annotation
    if ann is None:
        ann = ''
    if ann.strip().lower() == 'drill':
        return True
    words = (i.text or '').strip().split()
    if len(words) <= 1:
        # might result in a false positive but can just not drill it and remove
        return True
    return False


def get_drill_items():
    return list(sorted(filter(is_drill, get_highlights()), key=lambda h: h.dt))


class Krill(Interactive):
    def get_items(self):
        for i in get_drill_items():
            yield i.eid, todo(
                i.dt,

                heading=i.text,
                tags=['drill'],
                body=f'from {i.book.title}\n',
            )

if __name__ == '__main__':
    Krill.main()
