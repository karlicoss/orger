#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading


from my.media.movies import get_movies

class Movies(StaticView):
    def get_items(self):
        movies = get_movies()
        for m in movies:
            yield m.title, node(
                dt_heading(m.created, m.title),
                body=f'rating: {m.rating}',
            )


if __name__ == '__main__':
    Movies.main()
