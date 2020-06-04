#!/usr/bin/env python3
from itertools import chain
from typing import Iterable

from orger import Mirror
from orger.inorganic import node, link, OrgNode
from orger.common import dt_heading
from orger import pandoc

import my.roamresearch as roamresearch


# todo ^^ ^^ things are highlight?
def roam_text_to_org(text: str) -> str:
    """
    Cleans up Roam artifacts and adapts for better Org rendering
    """
    for f, t in [
            ('{{[[slider]]}}', ''),
    ]:
        text = text.replace(f, t)
    org = pandoc.to_org(text, from_='markdown')
    org = org.replace(r'\_', '_') # unescape, it's a bit aggressive..
    return org


def roam_note_to_org(node: roamresearch.Node, top=False) -> Iterable[OrgNode]:
    """
    Converts Roam node into Org-mode representation
    """
    children = list(chain.from_iterable(map(roam_note_to_org, node.children)))

    empty = len(node.body or '') == 0 and len(children) == 0
    if empty:
        # sometimes nodes are empty. two cases:
        # - no heading -- child notes, like accidental enter presses I guess
        # - heading    -- notes that haven't been created yet
        # just don't do anything in this case
        # todo make this logic conditional?
        return

    title = node.title
    # org-mode target allows jumping straight into
    # conveniently, links in Roam are already represented as [[link]] !
    target = '' if title is None else f'<<{title}>> '
    heading = target + link(title='x', url=node.permalink)

    todo = None
    body = node.body
    if body is not None:
        for t in ('TODO', 'DONE'):
            ts = '{{[[' + t + ']]}}'
            if body.startswith(ts):
                todo = t
                body = body[len(ts):]

        body = roam_text_to_org(body)

        lines = body.splitlines(keepends=True)
        # display first link of the body as the heading
        if len(lines) > 0:
            heading = heading + ' ' + lines[0]
            body = ''.join(lines[1:])
            if len(body) == 0:
                body = None

    if top:
        heading = dt_heading(node.created, heading)

    yield OrgNode(
        todo=todo,
        heading=heading,
        body=body,
        children=children,
    )


class RoamView(Mirror):
    def get_items(self):
        rr = roamresearch.roam()
        from concurrent.futures import ThreadPoolExecutor
        # todo might be an overkill, only using because of pandoc..
        with ThreadPoolExecutor() as pool:
            items = list(chain.from_iterable(pool.map(roam_note_to_org, rr.notes)))

        # move the ones with no children to the bottom
        items = list(sorted(items, key=lambda n: len(n.children), reverse=True))

        yield from items


if __name__ == '__main__':
    RoamView.main()
