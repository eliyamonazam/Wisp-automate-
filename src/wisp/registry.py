"""Maps config `type` strings to the trigger/action classes that implement them.

Built-ins are defined directly in this module. Third-party packages can add
their own triggers and actions *without touching this file* by registering
an entry point in their own `pyproject.toml`:

    [project.entry-points."wisp.triggers"]
    my_trigger = "my_package.triggers:MyTrigger"

    [project.entry-points."wisp.actions"]
    my_action = "my_package.actions:MyAction"

Once that package is installed alongside Wisp, `discover_plugins()` (called
once at CLI startup) picks it up automatically and it becomes usable from
any YAML config via `type: my_trigger` / `type: my_action`.
"""

from __future__ import annotations

import logging
from importlib.metadata import entry_points
from typing import Dict, Type

from .actions.base import Action
from .actions.file_ops import MoveByExtensionAction
from .actions.notify import NotifyAction
from .actions.shell import RunShellAction
from .triggers.base import Trigger
from .triggers.file_watch import FileCreatedTrigger
from .triggers.schedule import ScheduleTrigger

logger = logging.getLogger("wisp.registry")

TRIGGER_ENTRY_POINT_GROUP = "wisp.triggers"
ACTION_ENTRY_POINT_GROUP = "wisp.actions"

TRIGGER_REGISTRY: Dict[str, Type[Trigger]] = {
    "file_created": FileCreatedTrigger,
    "schedule": ScheduleTrigger,
}

ACTION_REGISTRY: Dict[str, Type[Action]] = {
    "move_by_extension": MoveByExtensionAction,
    "notify": NotifyAction,
    "shell": RunShellAction,
}


def _load_plugins(group: str, registry: Dict[str, type]) -> None:
    """Merge in any classes registered under entry-point `group`."""
    try:
        discovered = entry_points(group=group)
    except TypeError:  # pragma: no cover - fallback for very old Python
        discovered = entry_points().get(group, [])  # type: ignore[union-attr]

    for entry_point in discovered:
        try:
            registry[entry_point.name] = entry_point.load()
        except Exception:  # noqa: BLE001
            logger.exception(
                "Failed to load plugin '%s' from group '%s'", entry_point.name, group
            )


def discover_plugins() -> None:
    """Load third-party triggers/actions registered via entry points.

    Called once at CLI startup. Safe to call more than once.
    """
    _load_plugins(TRIGGER_ENTRY_POINT_GROUP, TRIGGER_REGISTRY)
    _load_plugins(ACTION_ENTRY_POINT_GROUP, ACTION_REGISTRY)
