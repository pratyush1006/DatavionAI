"""
Scheduler schedule contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from apps.datavionos.scheduler.job import (
    Job,
)
from apps.datavionos.scheduler.trigger import (
    Trigger,
)


class ScheduleStatus(
    StrEnum,
):
    """
    Schedule status.
    """

    ACTIVE = "active"

    PAUSED = "paused"

    DISABLED = "disabled"


@dataclass(
    frozen=True,
    slots=True,
)
class Schedule:
    """
    Immutable scheduler definition.
    """

    id: str

    job: Job

    trigger: Trigger

    status: ScheduleStatus = ScheduleStatus.ACTIVE


__all__ = [
    "Schedule",
    "ScheduleStatus",
]
