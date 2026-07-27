"""
Platform scheduler contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
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
    Job execution status.
    """

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TriggerType(
    StrEnum,
):
    """
    Supported trigger types.
    """

    IMMEDIATE = "immediate"
    DELAY = "delay"
    CRON = "cron"
    INTERVAL = "interval"


@dataclass(
    frozen=True,
    slots=True,
)
class JobTrigger:
    """
    Job scheduling trigger.
    """

    trigger_type: TriggerType

    run_at: datetime | None = None

    interval_seconds: int | None = None

    cron_expression: str | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class JobContext:
    """
    Execution context supplied to a job.
    """

    tenant_id: str | None = None

    organization_id: str | None = None

    correlation_id: str | None = None

    metadata: dict[str, Any] | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class JobResult:
    """
    Job execution result.
    """

    status: JobStatus

    started_at: datetime

    completed_at: datetime | None = None

    message: str | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class Job(
    Protocol,
):
    """
    Background job contract.
    """

    @property
    def name(
        self,
    ) -> str:
        """
        Job name.
        """

    async def execute(
        self,
        context: JobContext,
    ) -> JobResult:
        """
        Execute the job.
        """


@runtime_checkable
class Scheduler(
    Protocol,
):
    """
    Platform scheduler abstraction.
    """

    def schedule(
        self,
        job: Job,
        trigger: JobTrigger,
    ) -> str:
        """
        Schedule a job.

        Returns a scheduler-specific job
        identifier.
        """

    def cancel(
        self,
        job_id: str,
    ) -> bool:
        """
        Cancel a scheduled job.
        """

    def exists(
        self,
        job_id: str,
    ) -> bool:
        """
        Determine whether a scheduled
        job exists.
        """

    async def run_now(
        self,
        job: Job,
        *,
        context: JobContext | None = None,
    ) -> JobResult:
        """
        Execute a job immediately.
        """


__all__ = [
    "JobStatus",
    "TriggerType",
    "JobTrigger",
    "JobContext",
    "JobResult",
    "Job",
    "Scheduler",
]
