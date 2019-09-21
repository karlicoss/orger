#!/usr/bin/env python3
from orger import InteractiveView
from orger.inorganic import node, link, org_dt
from orger.org_utils import todo

from my.instapaper import get_todos # type: ignore


class IpTodos(InteractiveView):
    def get_items(self):
        for t in get_todos():
            # TODO move erorr handling to base renderer?
            yield t.uid, todo(
                dt=t.dt,

                heading=t.text,
                tags=['ip2org'],
                body=f'{t.note}\nfrom {link(title="ip", url=t.instapaper_link)}   {link(title=t.title, url=t.url)}',
            )


# TODO add some test
# def test():
#     org_tree = IpView().make_tree()
#     ll = pick_heading(org_tree, 'Life Extension Methods')
#     assert ll is not None
#     assert len(ll.children) > 4
#     assert any('sleep a lot' in c.item for c in ll.children)


if __name__ == '__main__':
    IpTodos.main()
