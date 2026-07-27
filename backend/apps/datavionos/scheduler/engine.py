"""
Scheduler engine contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.scheduler.execution import (
    SchedulerExecution,
)
from apps.datavionos.scheduler.schedule import (
    Schedule,
)


@runtime_checkable
class SchedulerEngine(
    Protocol,
):
    """
    Scheduler orchestration engine.
    """

    async def start(
        self,
    ) -> None:
        """
        Start the scheduler.
        """

    async def stop(
        self,
    ) -> None:
        """
        Stop the scheduler.
        """

    async def pause(
        self,
    ) -> None:
        """
        Pause scheduler processing.
        """

    async def resume(
        self,
    ) -> None:
        """
        Resume scheduler processing.
        """

    async def schedule(
        self,
        schedule: Schedule,
    ) -> None:
        """
        Register a schedule with the engine.
        """

    async def unschedule(
        self,
        schedule_id: str,
    ) -> None:
        """
        Remove a schedule from the engine.
        """

    async def execute(
        self,
        schedule: Schedule,
    ) -> SchedulerExecution:
        """
        Execute a schedule immediately.
        """

    async def tick(
        self,
    ) -> tuple[SchedulerExecution, ...]:
        """
        Process all schedules that are ready to execute.
        """


__all__ = [
    "SchedulerEngine",
]
