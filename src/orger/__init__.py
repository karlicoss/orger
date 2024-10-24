from typing import TYPE_CHECKING

from .org_view import Mirror, OrgWithKey, Queue

__all__ = [
    'Mirror',
    'OrgWithKey',
    'Queue',
]


if not TYPE_CHECKING:
    # TODO deprecate properly?
    InteractiveView = Queue
    StaticView = Mirror
