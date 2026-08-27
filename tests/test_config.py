import textwrap
from pathlib import Path

import pytest

from wisp.config import load_config


def test_load_valid_config(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        textwrap.dedent(
            """
            - name: organize-downloads
              trigger:
                type: file_created
                path: /tmp/in
              actions:
                - type: move_by_extension
                  target: /tmp/out
            """
        ),
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert len(config.pipelines) == 1
    pipeline = config.pipelines[0]
    assert pipeline.name == "organize-downloads"
    assert pipeline.trigger.type == "file_created"
    assert pipeline.trigger.options == {"path": "/tmp/in"}
    assert pipeline.actions[0].options == {"target": "/tmp/out"}


def test_pipeline_requires_at_least_one_action(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        textwrap.dedent(
            """
            - name: broken
              trigger:
                type: file_created
                path: /tmp/in
              actions: []
            """
        ),
        encoding="utf-8",
    )

    with pytest.raises(Exception):
        load_config(config_file)
