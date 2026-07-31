"""
Scheduler execution contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import (
    UTC,
    datetime,
)
from enum import StrEnum
from typing import (
    Any,
)

from apps.datavionos.scheduler.schedule import (
    Schedule,
)


class ExecutionStatus(
    StrEnum,
):
    """
    Status of a scheduler execution.
    """

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"

    TIMED_OUT = "timed_out"


@dataclass(
    frozen=True,
    slots=True,
)
class SchedulerExecution:
    """
    Immutable scheduler execution record.
    """

    id: str

    schedule: Schedule

    status: ExecutionStatus = ExecutionStatus.PENDING

    started_at: datetime = datetime.now(UTC)

    completed_at: datetime | None = None

    result: Any | None = None

    error: str | None = None


__all__ = [
    "ExecutionStatus",
    "SchedulerExecution",
]
