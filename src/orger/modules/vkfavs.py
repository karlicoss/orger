#!/usr/bin/env python3
from my.vk.favorites import Favorite, favorites

from orger import Mirror
from orger.common import dt_heading, error
from orger.inorganic import Quoted, link, node


class VkFavs(Mirror):
    def get_items(self) -> Mirror.Results:
        for f in favorites():
            if isinstance(f, Favorite):
                yield node(
                    heading=dt_heading(
                        f.dt,
                        f.title if f.url is None else link(url=f.url, title=f.title),
                    ),
                    body=Quoted(f.text),
                )
            else: # Exception
                yield error(f)


if __name__ == '__main__':
    VkFavs.main()
