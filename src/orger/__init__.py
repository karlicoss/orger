from typing import TYPE_CHECKING

from .org_view import Mirror, OrgWithKey, Queue, StaticView

if not TYPE_CHECKING:
    # TODO deprecate properly?
    InteractiveView = Queue
