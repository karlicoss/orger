#!/usr/bin/env python3
from my.rtm import active_tasks

from orger import Mirror
from orger.common import dt_heading
from orger.inorganic import node


class RtmView(Mirror):
    def get_items(self):
        for t in active_tasks():
            yield t.uid, node(
                dt_heading(t.time, t.title),
                tags=t.tags,
                body='\n'.join(t.notes),
            )

if __name__ == '__main__':
    RtmView.main()
