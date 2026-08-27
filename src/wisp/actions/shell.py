"""Shell-command action."""

from __future__ import annotations

import subprocess
from typing import Any, Dict

from .base import Action


class RunShellAction(Action):
    """Runs a shell command, formatting it with the event context first.

    Options:
        command: shell command to run, e.g. "cp {path} /tmp/backup/".
    """

    def __init__(self, command: str, **options: Any) -> None:
        super().__init__(command=command, **options)
        self.command = command

    def run(self, context: Dict[str, Any]) -> None:
        command = self.command.format(**context) if context else self.command
        subprocess.run(command, shell=True, check=False)
