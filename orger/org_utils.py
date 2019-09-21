from typing import NamedTuple, Sequence, Any, List, Tuple, Optional, TypeVar, Callable, Union, Type

from .inorganic import as_org_entry, OrgNode, org_dt, from_lazy

def pick_heading(root: OrgNode, text: str) -> Optional[OrgNode]:
    if text in from_lazy(root.heading):
        return root
    for ch in root.children:
        chr = pick_heading(ch, text)
        if chr is not None:
            return chr
    else:
        return None


from orger.inorganic import datetime2org
from datetime import datetime
def dt_heading(dt: Optional[datetime], heading: str):
    """
    Helper to inline datetime in heading
    """
    # TODO move to inorganic? not sure
    if dt is None:
        return heading
    else:
        return '[{}] '.format(datetime2org(dt)) + heading


# TODO not sure if belongs here
def todo(dt: datetime, **kwargs):
    """
    Helper to simplify creating todos
    """
    return OrgNode(
        todo='TODO',
        scheduled=dt.date(),
        properties={'CREATED': org_dt(dt, inactive=True)},
        **kwargs,
    )
