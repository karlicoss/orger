from typing import NamedTuple, Sequence, Any, List, Tuple, Optional, TypeVar, Callable, Union, Type

# TODO move OrgTree to inorganic? not sure about pick_heading
from .inorganic import as_org_entry, OrgNode, org_dt

# TODO compare before saving? not sure if necessary..

# TODO kython?...
T = TypeVar('T')
Lazy = Union[T, Callable[[], T]]

def from_lazy(x: Lazy[T], type_: Type[T]) -> T:
    if isinstance(x, type_):
        return x
    else:
        return x() # type: ignore

class OrgTree(NamedTuple):
    item_: Lazy[str]
    children: Sequence[Any] = ()

    @property
    def item(self) -> str:
        return from_lazy(self.item_, type_=str)

    def render_hier(self) -> List[Tuple[int, str]]:
        res = [(0, self.item)]
        for ch in self.children:
            # TODO make sure there is a space??
            # TODO shit, would be nice to tabulate?.. not sure
            res.extend((l + 1, x) for l, x in ch.render_hier())
        return res

    def render(self, level=0) -> str:
        rh = self.render_hier()
        rh = [(level + l, x) for l, x in rh]
        return '\n'.join('*' * l + (' ' if l > 0 else '') + x for l, x in rh)


def pick_heading(root: OrgTree, text: str) -> Optional[OrgTree]:
    if text in root.item:
        return root
    for ch in root.children:
        chr = pick_heading(ch, text)
        if chr is not None:
            return chr
    else:
        return None


# TODO hacky...
def as_org(todo=False, inline_created=True, **kwargs):
    res = as_org_entry(
        todo=todo,
        inline_created=inline_created,
        level=0,
        **kwargs,
    )
    return res


from orger.inorganic import datetime2org
from datetime import datetime
def dt_heading(dt: datetime, heading: str):
    """
    Helper to inline datetime in heading
    """
    # TODO move to inorganic? not sure
    return '[{}] '.format(datetime2org(dt)) + heading


# TODO not sure if belongs here
def todo(dt: datetime, **kwargs):
    pass
    """
    Helper to set some common todo item thing
    """
    return OrgNode(
        todo='TODO',
        scheduled=dt.date(),
        properties={'CREATED': org_dt(dt, inactive=True)},
        **kwargs,
    )


# TODO move tests to inorganic?
def test_render():
    xx = OrgNode(
        'file header',
        children=[
            OrgNode('subitem'),
        ],
    )
    assert xx.render() == """
file header
* subitem""".lstrip()


def test_render_2():
    xxx = OrgNode('TODO something')
    assert xxx.render(level=1) == "* TODO something"


def test_render_3():
    zzz = OrgNode(todo='TODO', heading='hi')
    assert zzz.render(level=1).startswith('* TODO hi')
