"""Abstract base class every action implementation must extend."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class Action(ABC):
    """A single step executed when a pipeline's trigger fires.

    Subclasses receive their YAML options as keyword arguments in
    `__init__` and must implement `run`, which receives the context
    dict produced by the trigger (e.g. `{"path": "..."}`).
    """

    def __init__(self, **options: Any) -> None:
        self.options = options

    @abstractmethod
    def run(self, context: Dict[str, Any]) -> None:
        """Execute this action given the triggering event's context."""
