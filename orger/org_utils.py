from typing import NamedTuple, Sequence, Any, List, Tuple, Optional, TypeVar, Callable, Union, Type

from .inorganic import as_org_entry, OrgNode, org_dt

def pick_heading(root: OrgNode, text: str) -> Optional[OrgNode]:
    if text in root.item:
        return root
    for ch in root.children:
        chr = pick_heading(ch, text)
        if chr is not None:
            return chr
    else:
        return None


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
    # test lazy property
    zzz = OrgNode(todo='TODO', heading=lambda: 'hi')
    assert zzz.render(level=1).startswith('* TODO hi')
