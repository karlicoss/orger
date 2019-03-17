from typing import NamedTuple, Sequence, Any, List, Tuple, Optional, TypeVar, Callable, Union, Type
from kython.org_tools import as_org_entry

# TODO FIXME compare before saving?

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
def as_org(**kwargs):
    return as_org_entry(
        todo=False,
        level=0,
        inline_created=True,
        **kwargs,
    ).strip()
