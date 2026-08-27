"""Maps config `type` strings to the trigger/action classes that implement them.

This is intentionally a plain dict rather than an entry-points-based plugin
system for now -- see the roadmap in README.md. Swapping it for
`importlib.metadata.entry_points()` later is a drop-in change that won't
affect anything else in the codebase.
"""

from __future__ import annotations

from typing import Dict, Type

from .actions.base import Action
from .actions.file_ops import MoveByExtensionAction
from .actions.notify import NotifyAction
from .actions.shell import RunShellAction
from .triggers.base import Trigger
from .triggers.file_watch import FileCreatedTrigger

TRIGGER_REGISTRY: Dict[str, Type[Trigger]] = {
    "file_created": FileCreatedTrigger,
}

ACTION_REGISTRY: Dict[str, Type[Action]] = {
    "move_by_extension": MoveByExtensionAction,
    "notify": NotifyAction,
    "shell": RunShellAction,
}
