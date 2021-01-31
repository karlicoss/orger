#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link, Quoted
from orger.common import dt_heading

import my.stackexchange.stexport as se


class Stackexchange(Mirror):
    def get_items(self) -> Mirror.Results:
        # TODO adapt for other stackexchange items
        se_data = se.site('stackoverflow')
        for q in se_data.questions:
            # TODO could emit items along with level, then it would look a bit more natural
            yield node(
                dt_heading(q.creation_date, link(url=q.link, title=q.title)),
                tags=q.tags,
                body=Quoted(q.body_markdown),
                # todo eh, would be useful to have md2org perhaps?
            )


if __name__ == '__main__':
    Stackexchange.main()


# todo how to simplify this even further? i.e. so you
# - don't need the class (just a function?)
#   maybe yield the marker object or something (policy?)
# - don't have to write main()
# - maybe not even do imports?
