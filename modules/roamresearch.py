#!/usr/bin/env python3

from orger import StaticView
from orger.inorganic import node, link, OrgNode
from orger.common import dt_heading

import my.roamresearch as roamresearch


def roam_note_to_org(node: roamresearch.Node) -> OrgNode:
    """
    Converts Roam node into Org-mode representation
    """
    title = node.title
    # org-mode target allows jumping straight into
    # conveniently, links in Roam are already represented as [[link]] !
    target = '' if title is None else f'<<{title}>> '
    heading = target + link(title='x', url=node.permalink)

    body = node.body
    if body is not None:
        lines = body.splitlines(keepends=True)
        # display first link of the body as the heading
        if len(lines) > 0:
            heading = heading + ' ' + lines[0]
            body = ''.join(lines[1:])
            if len(body) == 0:
                body = None
    return OrgNode(
        heading=heading,
        body=body,
        children=list(map(roam_note_to_org, node.children)),
    )


class RoamView(StaticView):
    def get_items(self):
        rr = roamresearch.roam()
        yield from map(roam_note_to_org, rr.nodes)


if __name__ == '__main__':
    RoamView.main()
