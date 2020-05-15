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


from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading

class PolarView(StaticView):
    def get_items(self):
        from my.reading import polar
        def make_item(res: polar.Result):
            if isinstance(res, polar.Error):
                # TODO could create error heading from exception automatically? take first line as heading and rest + traceback as the body
                return node(heading='ERROR ' + str(res)) # TODO priority A?
            else:
                b = res
                return node(
                    heading=dt_heading(
                        b.created,
                        # TODO apparently file: is not necessary if the path is absolute?
                        link(url=str(b.path), title=b.title),
                    ),
                    # tags=b.tags, # TODO?
                    children=[node(
                        heading=dt_heading(hl.created, hl.selection),
                        children=[node(
                            heading=dt_heading(c.created, c.text)
                        ) for c in hl.comments]
                    ) for hl in b.items]
                )
        for b in polar.get_entries():
            yield make_item(b)

# TODO convert html markup to org-mode


test = PolarView.make_test(
    heading='I missed the bit where he only restricted to spin'
)


if __name__ == '__main__':
    PolarView.main()

