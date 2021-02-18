#!/usr/bin/env python3
from orger import Mirror
from orger.inorganic import node, link
from orger.common import dt_heading

import my.twitter.all as twi


class TwitterLikesView(Mirror):
    def get_items(self) -> Mirror.Results:
        for tweet in twi.likes():
            # likes don't have timestamps (at least from GDPR export data)
            # TODO support it and handle None
            yield node(
                link(url=tweet.permalink, title='liked'),
                body=tweet.text
            )

if __name__ == '__main__':
    TwitterLikesView.main()
