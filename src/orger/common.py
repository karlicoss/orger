from __future__ import annotations

import logging
import sys
import traceback
import warnings
from datetime import datetime, tzinfo
from pathlib import Path
from typing import TYPE_CHECKING

import kloggy

if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

from .inorganic import OrgNode, TimestampStyle, timestamp, timestamp_with_style


# todo add error policy here?
class settings:
    DEFAULT_TIMESTAMP_STYLE = TimestampStyle.INACTIVE
    USE_PANDOC: bool = True


_timezones: set[tzinfo | None] = set()


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
            f"Seems that a mixture of timezones is used. Org-mode doesn't support timezones, so this might end up confusing: {_timezones} {tz} {heading}",
            stacklevel=2,
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

    @deprecated('Use kloggy.get_logger(name, default_level=level) instead.')
    def LazyLogger(name: str, *, level: int | str | None = None) -> logging.Logger:
        return kloggy.get_logger(name, default_level=level)

    @deprecated('Use kloggy.get_logger(name, default_level=level) instead.')
    def setup_logger(logger: str | logging.Logger, *, level: int | str | None = None) -> None:
        name = logger if isinstance(logger, str) else logger.name
        kloggy.get_logger(name, default_level=level)
