#!/usr/bin/env python3
from my.media.movies import get_movies

from orger import Overwrite
from orger.org_utils import OrgTree, as_org


class Movies(Overwrite):
    file = __file__
    logger_tag = 'movies'

    def get_items(self):
        movies = get_movies()
        for m in movies:
            yield (m.title, OrgTree(as_org(
                created=m.created,
                heading=m.title,
                body=f'rating: {m.rating}',
            )))


if __name__ == '__main__':
    Movies.main(default_to='movies.org') # TODO logger??
