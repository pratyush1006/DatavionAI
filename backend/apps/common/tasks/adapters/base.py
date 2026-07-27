"""
Base scheduler adapter contracts for DatavionOS.

Defines the abstraction layer between the DatavionOS task
framework and external scheduler providers.

Supported adapters:

- Celery Beat
- APScheduler
- Cloud Scheduler
- Kubernetes CronJobs

The kernel does not depend on any scheduler implementation.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)

from apps.common.tasks.scheduler import (
    ScheduleDefinition,
)


class BaseSchedulerAdapter(
    ABC,
):
    """
    Base contract for scheduler integrations.

    External scheduler implementations must provide:

    - schedule registration
    - schedule removal
    - scheduler synchronization
    """

    name: str = ""

    @abstractmethod
    def register(
        self,
        definition: ScheduleDefinition,
    ) -> None:
        """
        Register a scheduled task.
        """

    @abstractmethod
    def unregister(
        self,
        schedule_id: str,
    ) -> None:
        """
        Remove a scheduled task.
        """

    @abstractmethod
    def sync(
        self,
    ) -> None:
        """
        Synchronize schedules with scheduler backend.
        """


__all__: tuple[str, ...] = ("BaseSchedulerAdapter",)
