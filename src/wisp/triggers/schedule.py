"""Trigger that fires on a recurring schedule."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger as APCronTrigger
from apscheduler.triggers.interval import IntervalTrigger as APIntervalTrigger

from .base import Trigger


class ScheduleTrigger(Trigger):
    """Fires on a schedule -- either a cron expression or a fixed interval.

    Options (provide exactly one):
        cron: a standard 5-field cron expression, e.g. "*/5 * * * *"
        interval_seconds: fire every N seconds instead of using cron

    Fires with an empty context (`{}`). There's no "triggering file" for a
    schedule, so actions referencing `{path}` in their message/command will
    raise a KeyError -- schedule-driven pipelines should avoid that
    placeholder.
    """

    def __init__(
        self,
        cron: Optional[str] = None,
        interval_seconds: Optional[int] = None,
        **options: Any,
    ) -> None:
        super().__init__(cron=cron, interval_seconds=interval_seconds, **options)
        if not cron and not interval_seconds:
            raise ValueError("ScheduleTrigger requires either 'cron' or 'interval_seconds'")
        self.cron = cron
        self.interval_seconds = interval_seconds
        self._scheduler: Optional[BackgroundScheduler] = None

    def start(self, on_event: Callable[[Dict[str, Any]], None]) -> None:
        self._scheduler = BackgroundScheduler()
        trigger = (
            APCronTrigger.from_crontab(self.cron)
            if self.cron
            else APIntervalTrigger(seconds=self.interval_seconds)
        )
        self._scheduler.add_job(lambda: on_event({}), trigger)
        self._scheduler.start()

    def stop(self) -> None:
        if self._scheduler is not None:
            self._scheduler.shutdown(wait=False)
