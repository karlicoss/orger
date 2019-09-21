#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.org_utils import dt_heading

from my.instapaper import get_pages


class IpView(StaticView):
    def get_items(self):
        for page in get_pages():
            yield (page.bookmark.bid, node(
                heading=dt_heading(
                    page.bookmark.dt,
                    f'{link(title="ip", url=page.bookmark.instapaper_link)}   {link(title=page.bookmark.title, url=page.bookmark.url)}',
                ),
                children=[node(
                    heading=dt_heading(hl.dt, link(title="ip", url=page.bookmark.instapaper_link)),
                    body=hl.text,
                ) for hl in page.highlights]
            ))
        # TODO autostrip could be an option for formatter
        # TODO reverse order? not sure...
        # TODO unique id meaning that instapaper manages the item?
        # TODO spacing top level items could be option of dumper as well?
        # TODO better error handling, cooperate with org_tools


def test():
    from orger.org_utils import pick_heading
    org_tree = IpView().make_tree()
    ll = pick_heading(org_tree, 'Life Extension Methods')
    assert ll is not None
    assert len(ll.children) > 4
    assert any('sleep a lot' in c.render() for c in ll.children)

    assert org_tree.render().splitlines()[2].startswith('* [') # meh


if __name__ == '__main__':
    IpView.main()
