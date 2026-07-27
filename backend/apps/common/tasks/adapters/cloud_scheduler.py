"""
Cloud Scheduler adapter for DatavionOS.

Provides a cloud scheduler integration contract without
coupling the task kernel to any cloud provider SDK.

Supported deployment targets:

- Google Cloud Scheduler
- AWS EventBridge Scheduler
- Azure Scheduler services

Cloud-specific implementations belong in deployment/infrastructure
layers.
"""

from __future__ import annotations

from apps.common.tasks.adapters.base import (
    BaseSchedulerAdapter,
)
from apps.common.tasks.scheduler import (
    ScheduleDefinition,
)


class CloudSchedulerAdapter(
    BaseSchedulerAdapter,
):
    """
    Cloud scheduler integration adapter.

    Responsible for translating DatavionOS scheduling
    definitions into cloud scheduler jobs.

    No cloud SDK dependency is required inside the kernel.
    """

    name = "cloud_scheduler"

    def __init__(
        self,
    ) -> None:
        """
        Initialize adapter.
        """

        self._schedules: dict[
            str,
            ScheduleDefinition,
        ] = {}

    def register(
        self,
        definition: ScheduleDefinition,
    ) -> None:
        """
        Register a cloud scheduler job.

        Cloud API provisioning is handled by the
        infrastructure integration layer.
        """

        self._schedules[definition.schedule_id] = definition

    def unregister(
        self,
        schedule_id: str,
    ) -> None:
        """
        Remove cloud scheduler job.
        """

        self._schedules.pop(
            schedule_id,
            None,
        )

    def sync(
        self,
    ) -> None:
        """
        Synchronize schedules with cloud scheduler.

        Deployment examples:

        - AWS EventBridge Scheduler
        - Google Cloud Scheduler
        - Azure scheduling services
        """

        return


__all__: tuple[str, ...] = ("CloudSchedulerAdapter",)
