# Wisp

**Wisp** is a lightweight, extensible automation framework for your own machine — think "Zapier, but local and scriptable." Define pipelines in a small YAML file: when a **trigger** fires (a file appears, a schedule ticks), Wisp runs a chain of **actions** (move a file, run a command, send a notification).

```yaml
- name: organize-downloads
  trigger:
    type: file_created
    path: ~/Downloads
  actions:
    - type: move_by_extension
      target: ~/Sorted
    - type: notify
      message: "Sorted a new file: {path}"
```

```bash
wisp validate examples/organize_downloads.yaml
wisp run examples/organize_downloads.yaml
```

## Why Wisp

- **Declarative** — describe *what* should happen, not how to poll for it.
- **Small core, easy to extend** — triggers and actions are just classes with one method each (`start` / `run`). Adding a new one doesn't touch the engine.
- **No server, no account** — runs entirely on your machine, with a config file you own.

## Installation

```bash
git clone https://github.com/eliyamonazam/Wisp-automate-.git
cd Wisp-automate-
pip install -e ".[dev]"
```

## CLI commands

| Command | Description |
|---|---|
| `wisp validate <config.yaml>` | Check a config file for errors without running it |
| `wisp list <config.yaml>` | List the pipelines defined in a config file |
| `wisp run <config.yaml>` | Run all pipelines and wait for events (`Ctrl+C` to stop) |
| `wisp version` | Print the installed version |

## Built-in triggers

| Type | Options | Fires with |
|---|---|---|
| `file_created` | `path`, `recursive` (bool, default `false`) | `{"path": "<new file>"}` |

## Built-in actions

| Type | Options | Behavior |
|---|---|---|
| `move_by_extension` | `target` | Moves the triggering file into `<target>/<extension>/` |
| `notify` | `message` (supports `{path}`-style formatting) | Shows a desktop notification, falls back to stdout |
| `shell` | `command` (supports `{path}`-style formatting) | Runs a shell command |

## Architecture

```
config.yaml → PipelineConfig → Engine
                                  │
                     ┌────────────┴────────────┐
                     ▼                          ▼
                  Trigger.start(on_event)    Action.run(context)
                (watches / schedules)       (executes side effects)
```

Each pipeline pairs one trigger with a list of actions. The `Engine` looks up the trigger and action classes in `registry.py` by their `type` string, instantiates them with the options from YAML, and wires the trigger's callback to run every action in order.

## Extending Wisp

Adding a new trigger or action is three steps:

1. Subclass `Trigger` (implement `start`, optionally `stop`) or `Action` (implement `run`).
2. Register it in `src/wisp/registry.py` under a `type` string.
3. Reference that `type` string from your YAML config.

## Roadmap

- [ ] Plugin discovery via `entry_points` (third-party packages can register triggers/actions without editing this repo)
- [ ] Cron/schedule trigger (`APScheduler`)
- [ ] Webhook trigger (local HTTP listener)
- [ ] Run history persisted to SQLite, viewable via `wisp logs`
- [ ] Live status dashboard in the terminal (`rich`)

## Development

```bash
pip install -e ".[dev]"
pytest --cov=wisp
```

## License

MIT — see [LICENSE](LICENSE).
