from typing import NamedTuple, Sequence, Any, List, Tuple, Optional
from kython.org_tools import as_org_entry as as_org, link as org_link

# TODO FIXME compare before saving?

class OrgTree(NamedTuple):
    item: str
    children: Sequence[Any] = ()

    def render_hier(self) -> List[Tuple[int, str]]:
        res = [(0, self.item)]
        for ch in self.children:
            # TODO make sure there is a space??
            # TODO shit, would be nice to tabulate?.. not sure
            res.extend((l + 1, x) for l, x in ch.render_hier())
        return res

    def render(self) -> str:
        return '\n'.join('*' * l + ' ' + x for l, x in self.render_hier())


def pick_heading(root: OrgTree, text: str) -> Optional[OrgTree]:
    if text in root.item:
        return root
    for ch in root.children:
        chr = pick_heading(ch, text)
        if chr is not None:
            return chr
    else:
        return None
