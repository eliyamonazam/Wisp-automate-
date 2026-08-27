import time

import pytest

from wisp.triggers.schedule import ScheduleTrigger


def test_schedule_trigger_requires_cron_or_interval() -> None:
    with pytest.raises(ValueError):
        ScheduleTrigger()


def test_schedule_trigger_fires_on_interval() -> None:
    fired = []
    trigger = ScheduleTrigger(interval_seconds=1)
    trigger.start(lambda context: fired.append(context))
    try:
        deadline = time.time() + 3
        while not fired and time.time() < deadline:
            time.sleep(0.1)
    finally:
        trigger.stop()

    assert fired == [{}]
