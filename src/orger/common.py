from datetime import datetime
from typing import Optional
from pathlib import Path

from .inorganic import OrgNode, timestamp, timestamp_with_style, TimestampStyle


# todo add error policy here?
class settings:
    DEFAULT_TIMESTAMP_STYLE = TimestampStyle.INACTIVE
    USE_PANDOC: bool = True


_timezones = set()  # type: ignore
def dt_heading(dt: Optional[datetime], heading: str) -> str:
    """
    Helper to inline datetime in heading
    """
    # TODO move to inorganic? not sure
    if dt is None:
        return heading

    tz = dt.tzinfo
    # todo come up with a better way of reporting this..
    if tz not in _timezones and len(_timezones) > 0:
        import warnings
        warnings.warn(f"Seems that a mixture of timezones is used. Org-mode doesn't support timezones, so this might end up confusing: {_timezones} {tz} {heading}")
    _timezones.add(tz)

    return timestamp_with_style(dt=dt, style=settings.DEFAULT_TIMESTAMP_STYLE) + ' ' + heading


def error(e: Exception) -> OrgNode:
    import traceback
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
    import appdirs  # type: ignore[import-untyped]
    return Path(appdirs.user_config_dir('orger'))


from .logging_helper import LazyLogger, setup_logger  # legacy imports for bwd compatibility
