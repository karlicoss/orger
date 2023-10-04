#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading

from my.rtm import active_tasks


class RtmView(StaticView):
    def get_items(self):
        for t in active_tasks():
            yield t.uid, node(
                dt_heading(t.time, t.title),
                tags=t.tags,
                body='\n'.join(t.notes),
            )

if __name__ == '__main__':
    RtmView.main()
