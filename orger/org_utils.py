from typing import NamedTuple, Sequence, Any, List, Tuple, Optional, TypeVar, Callable, Union, Type

# TODO move OrgTree to inorganic? not sure about pick_heading
from .inorganic import as_org_entry

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


from typing import NamedTuple, Optional, Sequence, Dict, Mapping, Any
# TODO what was the need for lazy?
class OrgNode(NamedTuple):
    heading: str
    todo: Optional[str] = None
    tags: Sequence[str] = ()
    properties: Optional[Mapping[str, str]] = None
    body: str=''
    children: Sequence[Any]=() # mypy wouldn't allow recursive type here...

    def render_self(self) -> str:
        # TODO FIXME properties
        return as_org(
            heading=self.heading, # TODO FIXME todo keyword?
            tags=self.tags,
            body=self.body,
            force_no_created=True,
        )

    def render_hier(self) -> List[Tuple[int, str]]:
        res = [(0, self.render_self())]
        for ch in self.children:
            # TODO make sure there is a space??
            # TODO shit, would be nice to tabulate?.. not sure
            res.extend((l + 1, x) for l, x in ch.render_hier())
        return res

    def render(self, level=0) -> str:
        rh = self.render_hier()
        rh = [(level + l, x) for l, x in rh]
        return '\n'.join('*' * l + (' ' if l > 0 else '') + x for l, x in rh)

# TODO level -- I guess gonna be implicit...



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


def test_render():
    xx = OrgTree(
        'file header',
        [
            OrgTree('subitem'),
        ],
    )
    assert xx.render() == """
file header
* subitem""".lstrip()


def test_render_2():
    xxx = OrgTree('TODO something')
    assert xxx.render(level=1) == "* TODO something"


def test_render_3():
    zzz = OrgTree(as_org(todo=True, heading='hi', inline_created=False))
    assert zzz.render(level=1).startswith('* TODO hi')
