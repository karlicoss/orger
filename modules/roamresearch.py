#!/usr/bin/env python3

from orger import StaticView
from orger.inorganic import node, link, OrgNode
from orger.common import dt_heading

import my.roamresearch as roamresearch


def roam_to_org(node: roamresearch.Node) -> OrgNode:
    return OrgNode(
        heading=link(title=node.title, url=node.permalink),
        children=list(map(roam_to_org, node.children)),
    )
    # TODO inline links

class RoamView(StaticView):
    def get_items(self):
        rr = roamresearch.roam()
        yield from map(roam_to_org, rr.nodes)


if __name__ == '__main__':
    RoamView.main()
