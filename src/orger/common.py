from datetime import datetime
from typing import Optional
from pathlib import Path

from .inorganic import OrgNode, timestamp, timestamp_with_style, TimestampStyle


# todo add error policy here?
class settings:
    DEFAULT_TIMESTAMP_STYLE = TimestampStyle.INACTIVE
    USE_PANDOC: bool = True


def dt_heading(dt: Optional[datetime], heading: str) -> str:
    """
    Helper to inline datetime in heading
    """
    # TODO move to inorganic? not sure
    if dt is None:
        return heading
    else:
        return timestamp_with_style(dt=dt, style=settings.DEFAULT_TIMESTAMP_STYLE) + ' ' + heading


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
    props = kwargs.get('properties', {})
    props.update({'CREATED': timestamp(dt, inactive=True)})
    kwargs['properties'] = props
    return OrgNode(
        todo='TODO',
        scheduled=dt.date(),
        **kwargs,
    )


# todo use klogging2?
from .klogging import LazyLogger, setup_logger


def orger_user_dir() -> Path:
    import appdirs # type: ignore[import]
    return Path(appdirs.user_config_dir('orger'))
