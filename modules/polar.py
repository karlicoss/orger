#!/usr/bin/env python3
"""
Example output:


* [2018-11-28 Wed 22:04] [Baez] Lectures on Classical Mechanics.pdf 12nwnBFvng-[Baez] Lectures on Classical Mechanics.pdf
...
* [2019-01-20 Sun 14:00] [Woit] Quantum Theory, Groups and Representations.pdf 12LWfRf8Gf-[Woit] Quantum Theory, Groups and Representations.pdf
** [2019-01-20 Sun 14:34]  An important corollary of Schurs lemma is the following characterization of irreducible representations of G when G is commutative.
** [2019-01-20 Sun 14:40]  As such it has a differential, which  is  a  linear  map  from  the  tangent  space  at  the  identity  of U (1)  (which here is i R ) to the tangent space at the identity of GL ( n, C ) (which is the space M ( n, C ) of n by n complex matrices).  Th e tangent space at the identity of a Lie group is called a Lie algebra
** [2019-01-20 Sun 14:47]  n general [ Q,H ] 6 = 0, with Q then gen- erating a unitary action on H that does not commute with time evolution and does not imply a conservation law
** [2019-01-20 Sun 14:49]   In the limit N one can make contact with classical notions of spinning objects and angular momentum, but the spin
** [2019-01-20 Sun 15:25]   For further reading
*** [2019-01-20 Sun 15:25] Right. so here I think I missed the bit where he only restricted to spin 1/2
"""


from orger import Mirror
from orger.inorganic import node, link, docview_link, OrgNode, literal
from orger.common import dt_heading, error
from orger import pandoc


class PolarView(Mirror):
    def get_items(self) -> Mirror.Results:
        from my import polar

        def make_comment(c: polar.Comment) -> OrgNode:
            text = pandoc.to_org(data=c.text, from_='html', logger=self.logger)
            return node(
                heading=dt_heading(c.created, text.splitlines()[0]),
                body=text,
            )

        def make_highlight(book: polar.Book, hl: polar.Highlight) -> OrgNode:
            page1 = hl.page
            selection = hl.selection
            # ugh, not sure why are they so fucked in Polar..
            selection = selection.replace('\n', ' ')
            return node(
                heading=dt_heading(
                    hl.created,
                    docview_link(path=book.path, title=f'page {page1}', page1=page1),
                ),
                body=literal(selection),
                tags=hl.tags,
                properties=None if hl.color is None else {'POLAR_COLOR': hex2name(hl.color)},
                children=[make_comment(c) for c in hl.comments],
            )

        def make_item(res: polar.Result) -> OrgNode:
            if isinstance(res, Exception):
                return error(res)
            else:
                book = res
                return node(
                    heading=dt_heading(
                        book.created,
                        docview_link(path=book.path, title=book.title),
                    ),
                    tags=book.tags,
                    children=[make_highlight(book=book, hl=hl) for hl in book.items],
                )
        for res in polar.get_entries():
            yield make_item(res)

# not sure about this.. r.g. if the users define their own colors in the future
def hex2name(hexc: str) -> str:
    m = {
        '#ff6900': 'orange',
        '#9900ef': 'violet',
    }
    return m.get(hexc.lower(), hexc)

test = PolarView.make_test(
    heading='I missed the bit where he only restricted to spin'
)



if __name__ == '__main__':
    PolarView.main()

