"""
Scheduler registry contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.scheduler.schedule import (
    Schedule,
)


@runtime_checkable
class SchedulerRegistry(
    Protocol,
):
    """
    Registry of scheduler definitions.
    """

    async def register(
        self,
        schedule: Schedule,
    ) -> None:
        """
        Register a schedule.
        """

    async def unregister(
        self,
        schedule_id: str,
    ) -> None:
        """
        Remove a schedule.
        """

    async def get(
        self,
        schedule_id: str,
    ) -> Schedule | None:
        """
        Return a schedule by identifier.
        """

    async def list(
        self,
    ) -> tuple[Schedule, ...]:
        """
        Return all registered schedules.
        """

    async def exists(
        self,
        schedule_id: str,
    ) -> bool:
        """
        Determine whether a schedule exists.
        """


__all__ = [
    "SchedulerRegistry",
]
