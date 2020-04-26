#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
from typing import NamedTuple, Sequence, Any

class Highlight(NamedTuple):
    json: Any

    @property
    def text(self) -> str:
        return self.json['quote']

    @property
    def created(self) -> datetime:
        return datetime.strptime(self.json['created_at'], '%Y-%m-%d %H:%M:%S')


class Article(NamedTuple):
    json: Any

    @property
    def url(self) -> str:
        return self.json['given_url']

    @property
    def title(self) -> str:
        return self.json['given_title']

    @property
    def pocket_link(self) -> str:
        return 'https://app.getpocket.com/read/' + self.json['item_id']

    @property
    def added(self) -> datetime:
        return datetime.fromtimestamp(int(self.json['time_added']))

    @property
    def highlights(self) -> Sequence[Highlight]:
        raw = self.json.get('annotations', [])
        return list(map(Highlight, raw))

    # TODO add tags?


def get_articles(json_path: Path) -> Sequence[Article]:
    import json
    raw = json.loads(json_path.read_text())['list']
    return list(map(Article, raw.values()))

from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading


class PocketView(StaticView):
    def get_items(self):
        export_file = self.cmdline_args.file
        for a in get_articles(export_file):
            yield node(
                heading=dt_heading(
                    a.added,
                    link(title='pocket', url=a.pocket_link)  + ' · ' + link(title=a.title, url=a.url)
                ),
                children=[node(
                    heading=dt_heading(hl.created, hl.text)
                ) for hl in a.highlights]
            )


def setup_parser(p):
    p.add_argument('--file', type=Path, help='JSON file from API export', required=True)


if __name__ == '__main__':
    PocketView.main(setup_parser=setup_parser)
