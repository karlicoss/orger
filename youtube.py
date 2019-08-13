#!/usr/bin/env python3
from my.media.youtube import get_watched

from kython import group_by_key
from kython.org_tools import link as org_link

from orger import Overwrite
from orger.org_utils import OrgTree, as_org


class YoutubeView(Overwrite):
    file = __file__
    logger_tag = 'youtube-view'

    def get_items(self):
        watched = get_watched()
        items = [max(group, key=lambda w: w.when) for _, group in group_by_key(watched, key=lambda w: w.url).items()]
        items = sorted(items, key=lambda w: w.when)
        # TODO for each url only take latest?
        for item in items:
            yield (item.url, OrgTree(as_org(
                created=item.when,
                heading=org_link(title=item.title, url=item.url),
            )))

if __name__ == '__main__':
    YoutubeView.main(default_to='youtube.org')
