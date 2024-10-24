from __future__ import annotations

import traceback
import warnings
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from .inorganic import OrgNode, TimestampStyle, timestamp, timestamp_with_style


# todo add error policy here?
class settings:
    DEFAULT_TIMESTAMP_STYLE = TimestampStyle.INACTIVE
    USE_PANDOC: bool = True


_timezones = set()  # type: ignore


def dt_heading(dt: datetime | None, heading: str) -> str:
    """
    Helper to inline datetime in heading
    """
    # TODO move to inorganic? not sure
    if dt is None:
        return heading

    tz = dt.tzinfo
    # todo come up with a better way of reporting this..
    if tz not in _timezones and len(_timezones) > 0:
        warnings.warn(
            f"Seems that a mixture of timezones is used. Org-mode doesn't support timezones, so this might end up confusing: {_timezones} {tz} {heading}"
        )
    _timezones.add(tz)

    return timestamp_with_style(dt=dt, style=settings.DEFAULT_TIMESTAMP_STYLE) + ' ' + heading


def error(e: Exception) -> OrgNode:
    return OrgNode(
        heading="ERROR!",
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


def orger_user_dir() -> Path:
    import platformdirs

    return Path(platformdirs.user_config_dir('orger'))


if not TYPE_CHECKING:
    # legacy imports for bwd compatibility
    from .logging_helper import LazyLogger, setup_logger  # noqa: F401
