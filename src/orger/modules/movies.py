#!/usr/bin/env python3
from my.media.imdb import get_movies

from orger import Mirror
from orger.common import dt_heading
from orger.inorganic import node


class Movies(Mirror):
    def get_items(self):
        movies = get_movies()
        for m in movies:
            yield (
                m.title,
                node(
                    dt_heading(m.created, m.title),
                    body=f'rating: {m.rating}',
                ),
            )


if __name__ == '__main__':
    Movies.main()
