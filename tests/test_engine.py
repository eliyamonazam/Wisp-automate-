from typing import Any, ClassVar, Dict, List

from wisp import registry
from wisp.config import WispConfig
from wisp.engine import Engine


class _FakeTrigger:
    def __init__(self, **options: Any) -> None:
        self.options = options

    def start(self, on_event) -> None:  # noqa: ANN001
        # Simulate a single event firing immediately.
        on_event({"path": "/tmp/fake.txt"})

    def stop(self) -> None:
        pass


class _FakeAction:
    calls: ClassVar[List[Dict[str, Any]]] = []

    def __init__(self, **options: Any) -> None:
        self.options = options

    def run(self, context: Dict[str, Any]) -> None:
        _FakeAction.calls.append(context)


def test_engine_wires_trigger_to_action(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setitem(registry.TRIGGER_REGISTRY, "fake_trigger", _FakeTrigger)
    monkeypatch.setitem(registry.ACTION_REGISTRY, "fake_action", _FakeAction)
    _FakeAction.calls = []

    config = WispConfig(
        pipelines=[
            {
                "name": "test-pipeline",
                "trigger": {"type": "fake_trigger"},
                "actions": [{"type": "fake_action"}],
            }
        ]
    )

    engine = Engine(config)
    engine.run()

    assert _FakeAction.calls == [{"path": "/tmp/fake.txt"}]


def test_engine_raises_on_unknown_trigger() -> None:
    config = WispConfig(
        pipelines=[
            {
                "name": "bad-trigger",
                "trigger": {"type": "does_not_exist"},
                "actions": [{"type": "shell", "command": "echo hi"}],
            }
        ]
    )
    engine = Engine(config)
    try:
        engine.run()
        assert False, "expected ValueError"
    except ValueError:
        pass
