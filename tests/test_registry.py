from types import SimpleNamespace

from wisp import registry


class _DummyAction:
    pass


def test_load_plugins_merges_entry_points(monkeypatch) -> None:  # noqa: ANN001
    fake_entry_point = SimpleNamespace(name="dummy_action", load=lambda: _DummyAction)

    def fake_entry_points(group: str):
        if group == registry.ACTION_ENTRY_POINT_GROUP:
            return [fake_entry_point]
        return []

    monkeypatch.setattr(registry, "entry_points", fake_entry_points)

    test_registry: dict = {}
    registry._load_plugins(registry.ACTION_ENTRY_POINT_GROUP, test_registry)

    assert test_registry["dummy_action"] is _DummyAction


def test_load_plugins_ignores_broken_entry_point(monkeypatch, caplog) -> None:  # noqa: ANN001
    def _boom():
        raise ImportError("nope")

    broken_entry_point = SimpleNamespace(name="broken", load=_boom)

    def fake_entry_points(group: str):
        return [broken_entry_point]

    monkeypatch.setattr(registry, "entry_points", fake_entry_points)

    test_registry: dict = {}
    registry._load_plugins("some.group", test_registry)

    assert test_registry == {}
