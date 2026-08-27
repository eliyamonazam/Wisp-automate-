"""Configuration models and YAML loading for Wisp pipelines."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Union

import yaml
from pydantic import BaseModel, ConfigDict, field_validator


class _FlexibleModel(BaseModel):
    """Base model that accepts arbitrary extra fields.

    Trigger and action configs share a `type` field plus an open-ended
    set of options (e.g. `path`, `target`, `message`). Rather than force
    every trigger/action to declare its own top-level pydantic model,
    we accept any extra keys and expose them as a plain dict via
    `.options`, which trigger/action classes unpack as keyword arguments.
    """

    model_config = ConfigDict(extra="allow")

    @property
    def options(self) -> Dict[str, Any]:
        return self.model_dump(exclude={"type"})


class TriggerConfig(_FlexibleModel):
    type: str


class ActionConfig(_FlexibleModel):
    type: str


class PipelineConfig(BaseModel):
    name: str
    trigger: TriggerConfig
    actions: List[ActionConfig]

    @field_validator("actions")
    @classmethod
    def _at_least_one_action(cls, value: List[ActionConfig]) -> List[ActionConfig]:
        if not value:
            raise ValueError("Each pipeline must define at least one action")
        return value


class WispConfig(BaseModel):
    pipelines: List[PipelineConfig]


def load_config(path: Union[str, Path]) -> WispConfig:
    """Load and validate a Wisp YAML config file.

    The config file may be a bare list of pipelines (the common case) or
    an object with a top-level `pipelines` key.
    """
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or []
    if isinstance(raw, list):
        raw = {"pipelines": raw}
    return WispConfig(**raw)
