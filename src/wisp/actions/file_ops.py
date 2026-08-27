"""File-system actions."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Dict

from .base import Action


class MoveByExtensionAction(Action):
    """Moves the triggering file into `<target>/<extension>/`.

    Options:
        target: base directory to sort files into.
    """

    def __init__(self, target: str, **options: Any) -> None:
        super().__init__(target=target, **options)
        self.target = Path(target).expanduser()

    def run(self, context: Dict[str, Any]) -> None:
        source = Path(context["path"])
        if not source.exists():
            return
        extension = source.suffix.lstrip(".") or "other"
        destination_dir = self.target / extension
        destination_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination_dir / source.name))
