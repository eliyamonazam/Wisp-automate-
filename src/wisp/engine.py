"""The engine that wires triggers to their pipelines' actions and runs them."""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List

from .config import PipelineConfig, WispConfig
from .registry import ACTION_REGISTRY, TRIGGER_REGISTRY
from .triggers.base import Trigger

logger = logging.getLogger("wisp.engine")


class Engine:
    """Instantiates triggers/actions from config and runs pipelines."""

    def __init__(self, config: WispConfig) -> None:
        self.config = config
        self._triggers: List[Trigger] = []

    def _build_handler(self, pipeline: PipelineConfig) -> Callable[[Dict[str, Any]], None]:
        actions = []
        for action_cfg in pipeline.actions:
            action_cls = ACTION_REGISTRY.get(action_cfg.type)
            if action_cls is None:
                raise ValueError(f"Unknown action type: {action_cfg.type!r}")
            actions.append(action_cls(**action_cfg.options))

        def handler(context: Dict[str, Any]) -> None:
            logger.info("Pipeline '%s' triggered", pipeline.name)
            for action in actions:
                try:
                    action.run(context)
                except Exception:  # noqa: BLE001
                    logger.exception(
                        "Action %s in pipeline '%s' failed",
                        type(action).__name__,
                        pipeline.name,
                    )

        return handler

    def run(self) -> None:
        """Start every pipeline's trigger. Non-blocking."""
        for pipeline in self.config.pipelines:
            trigger_cls = TRIGGER_REGISTRY.get(pipeline.trigger.type)
            if trigger_cls is None:
                raise ValueError(f"Unknown trigger type: {pipeline.trigger.type!r}")
            trigger = trigger_cls(**pipeline.trigger.options)
            trigger.start(self._build_handler(pipeline))
            self._triggers.append(trigger)
        logger.info("Wisp is running with %d pipeline(s)", len(self.config.pipelines))

    def stop(self) -> None:
        """Stop every running trigger and release resources."""
        for trigger in self._triggers:
            trigger.stop()
        self._triggers.clear()
