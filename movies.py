#!/usr/bin/env python3
from orger import View
from orger.inorganic import node, link
from orger.org_utils import dt_heading


from my.media.movies import get_movies

class Movies(View):
    def get_items(self):
        movies = get_movies()
        for m in movies:
            yield m.title, node(
                dt_heading(m.created, m.title),
                body=f'rating: {m.rating}',
            )


if __name__ == '__main__':
    Movies.main()
