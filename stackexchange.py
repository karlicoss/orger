#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.org_utils import dt_heading

import my.stackexchange as se


class Stackexchange(StaticView):
    def get_items(self):
        # TODO adapt for other stackexchange items
        se_data = se.get_data()
        for q in se_data.questions:
            # TODO could emit items along with level, then it would look a bit more natural
            yield node(
                dt_heading(q.creation_date, link(url=q.link, title=q.title)),
                tags=q.tags,
                body=q.body_markdown, # TODO eh, would be useful to have md2org perhaps?
            )


if __name__ == '__main__':
    Stackexchange.main()
