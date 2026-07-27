"""
Scheduler job contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class JobStatus(
    StrEnum,
):
    """
    Status of a scheduled job.
    """

    PENDING = "pending"

    SCHEDULED = "scheduled"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


@dataclass(
    frozen=True,
    slots=True,
)
class Job:
    """
    Immutable scheduled job definition.
    """

    id: str

    name: str

    handler: str

    status: JobStatus = JobStatus.PENDING

    metadata: dict[str, Any] | None = None


@runtime_checkable
class JobHandler(
    Protocol,
):
    """
    Executes a scheduled job.
    """

    async def execute(
        self,
        job: Job,
    ) -> None:
        """
        Execute the scheduled job.
        """


__all__ = [
    "Job",
    "JobHandler",
    "JobStatus",
]
