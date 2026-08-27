"""Trigger that fires whenever a new file appears in a watched directory."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, Optional

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .base import Trigger


class _CreatedHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        self._callback = callback

    def on_created(self, event) -> None:  # noqa: ANN001
        if not event.is_directory:
            self._callback({"path": event.src_path})


class FileCreatedTrigger(Trigger):
    """Fires with `{"path": <new file path>}` when a file is created.

    Options:
        path: directory to watch (created automatically if missing).
        recursive: whether to watch subdirectories too. Default: False.
    """

    def __init__(self, path: str, recursive: bool = False, **options: Any) -> None:
        super().__init__(path=path, recursive=recursive, **options)
        self.path = Path(path).expanduser()
        self.recursive = recursive
        self._observer: Optional[Observer] = None

    def start(self, on_event: Callable[[Dict[str, Any]], None]) -> None:
        self.path.mkdir(parents=True, exist_ok=True)
        handler = _CreatedHandler(on_event)
        self._observer = Observer()
        self._observer.schedule(handler, str(self.path), recursive=self.recursive)
        self._observer.start()

    def stop(self) -> None:
        if self._observer is not None:
            self._observer.stop()
            self._observer.join()
