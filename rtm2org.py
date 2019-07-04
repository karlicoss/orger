#!/usr/bin/env python3
from kython.org_tools import link as org_link

from orger.org_view import OrgViewOverwrite, OrgWithKey
from orger.org_utils import OrgTree, as_org, pick_heading

from my.rtm import get_active_tasks


class RtmView(OrgViewOverwrite):
    file = __file__
    logger_tag = 'rtm-view'

    def get_items(self):
        for t in get_active_tasks():
            yield (
                t.uid,
                OrgTree(as_org(
                    heading=t.title,
                    body='\n'.join(t.notes),
                    created=t.time,
                    tags=t.tags,
                )),
            )


def main():
    RtmView.main(default_to='rtm.org')

if __name__ == '__main__':
    main()
