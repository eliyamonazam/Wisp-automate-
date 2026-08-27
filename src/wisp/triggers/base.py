"""Abstract base class every trigger implementation must extend."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict


class Trigger(ABC):
    """A source of events that kicks off a pipeline.

    Subclasses receive their YAML options as keyword arguments in
    `__init__` and must implement `start`, which begins watching /
    scheduling and calls `on_event(context)` for every occurrence.
    """

    def __init__(self, **options: Any) -> None:
        self.options = options

    @abstractmethod
    def start(self, on_event: Callable[[Dict[str, Any]], None]) -> None:
        """Begin listening for events, invoking `on_event` for each one."""

    def stop(self) -> None:
        """Release any resources (threads, observers, timers). Optional."""
