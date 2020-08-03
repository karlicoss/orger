#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading
import traceback

from my.vk.favorites import favorites, Favorite

class VkFavs(StaticView):
    def get_items(self):
        for f in favorites():
            if isinstance(f, Favorite):
                yield node(
                    heading=dt_heading(
                        f.dt,
                        f.title if f.url is None else link(url=f.url, title=f.title),
                    ),
                    body=f.text,
                )
            else: # error
                yield node(
                    heading=f'ERROR!',
                    body='\n'.join(traceback.format_exception(Exception, f, None)),
                )


if __name__ == '__main__':
    VkFavs.main()
