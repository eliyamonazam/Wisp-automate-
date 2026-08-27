"""Desktop notification action, with a console fallback."""

from __future__ import annotations

import platform
import subprocess
from typing import Any, Dict

from .base import Action


class NotifyAction(Action):
    """Shows a desktop notification (falls back to printing to stdout).

    Options:
        message: text to show. May reference context keys, e.g.
            "New file: {path}".
    """

    def __init__(self, message: str, **options: Any) -> None:
        super().__init__(message=message, **options)
        self.message = message

    def run(self, context: Dict[str, Any]) -> None:
        text = self.message.format(**context) if context else self.message
        system = platform.system()
        try:
            if system == "Darwin":
                subprocess.run(
                    ["osascript", "-e", f'display notification "{text}" with title "Wisp"'],
                    check=False,
                )
            elif system == "Linux":
                subprocess.run(["notify-send", "Wisp", text], check=False)
            else:
                print(f"[Wisp] {text}")
        except FileNotFoundError:
            print(f"[Wisp] {text}")
