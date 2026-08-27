"""Command-line interface for Wisp."""

from __future__ import annotations

import logging
import signal
import sys
import time
from pathlib import Path
from types import FrameType
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from .config import load_config
from .engine import Engine

app = typer.Typer(
    help="Wisp: run local automation pipelines defined in a YAML config.",
    no_args_is_help=True,
)
console = Console()


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(console=console, show_path=False)],
    )


@app.command()
def validate(
    config_path: Path = typer.Argument(..., help="Path to the YAML config file."),
) -> None:
    """Validate a config file without running it."""
    try:
        config = load_config(config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[bold red]Invalid config:[/] {exc}")
        raise typer.Exit(code=1)
    console.print(f"[bold green]✓[/] Config is valid — {len(config.pipelines)} pipeline(s) found.")


@app.command(name="list")
def list_pipelines(
    config_path: Path = typer.Argument(..., help="Path to the YAML config file."),
) -> None:
    """List the pipelines defined in a config file."""
    config = load_config(config_path)
    table = Table(title="Pipelines")
    table.add_column("Name")
    table.add_column("Trigger")
    table.add_column("Actions")
    for pipeline in config.pipelines:
        table.add_row(pipeline.name, pipeline.trigger.type, str(len(pipeline.actions)))
    console.print(table)


@app.command()
def run(
    config_path: Path = typer.Argument(..., help="Path to the YAML config file."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show debug-level logs."),
) -> None:
    """Run pipelines and wait for events (Ctrl+C to stop)."""
    _setup_logging(verbose)
    config = load_config(config_path)
    engine = Engine(config)
    engine.run()

    def _handle_stop(signum: int, frame: Optional[FrameType]) -> None:
        console.print("\n[yellow]Stopping...[/]")
        engine.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, _handle_stop)
    signal.signal(signal.SIGTERM, _handle_stop)

    while True:
        time.sleep(1)


@app.command()
def version() -> None:
    """Show the installed Wisp version."""
    from . import __version__

    console.print(f"Wisp v{__version__}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
