"""
Scheduler dispatcher contracts.
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
class SchedulerDispatcher(
    Protocol,
):
    """
    Dispatches scheduled work for execution.
    """

    async def dispatch(
        self,
        schedule: Schedule,
    ) -> SchedulerExecution:
        """
        Dispatch a schedule for execution.
        """

    async def dispatch_batch(
        self,
        schedules: tuple[Schedule, ...],
    ) -> tuple[SchedulerExecution, ...]:
        """
        Dispatch multiple schedules.
        """


__all__ = [
    "SchedulerDispatcher",
]
