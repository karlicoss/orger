from datetime import datetime
from typing import Optional

from .inorganic import OrgNode, timestamp


def dt_heading(dt: Optional[datetime], heading: str):
    """
    Helper to inline datetime in heading
    """
    # TODO move to inorganic? not sure
    if dt is None:
        return heading
    else:
        return timestamp(dt, inactive=True) + ' ' + heading


def error(e: Exception) -> OrgNode:
    import traceback
    return OrgNode(
        heading=f"ERROR!",
        body='\n'.join(traceback.format_exception(Exception, e, None)),
    )


# TODO not sure if belongs here
def todo(dt: datetime, **kwargs):
    """
    Helper to simplify creating todos
    """
    return OrgNode(
        todo='TODO',
        scheduled=dt.date(),
        properties={'CREATED': timestamp(dt, inactive=True)},
        **kwargs,
    )


from .klogging import LazyLogger, setup_logger
