"""
APScheduler adapter for DatavionOS.

Provides an APScheduler integration contract without coupling
the task kernel directly to APScheduler.

The scheduler dependency should be provided by the deployment
layer.

Supported environments:

- Django application server
- Dedicated worker service
- Background scheduler process
"""

from __future__ import annotations

from apps.common.tasks.adapters.base import (
    BaseSchedulerAdapter,
)
from apps.common.tasks.scheduler import (
    ScheduleDefinition,
)


class APSchedulerAdapter(
    BaseSchedulerAdapter,
):
    """
    APScheduler integration adapter.

    Translates DatavionOS schedule definitions into
    APScheduler-compatible definitions.

    The APScheduler package remains outside the kernel.
    """

    name = "apscheduler"

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
        Register a schedule.

        Actual APScheduler job creation is handled
        by deployment integration.
        """

        self._schedules[definition.schedule_id] = definition

    def unregister(
        self,
        schedule_id: str,
    ) -> None:
        """
        Remove scheduled task.
        """

        self._schedules.pop(
            schedule_id,
            None,
        )

    def sync(
        self,
    ) -> None:
        """
        Synchronize schedules with APScheduler.

        Deployment layer example:

            scheduler.add_job(
                func,
                trigger,
            )

        """

        return


__all__: tuple[str, ...] = ("APSchedulerAdapter",)
