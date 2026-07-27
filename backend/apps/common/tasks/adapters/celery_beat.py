"""
Celery Beat scheduler adapter for DatavionOS.

Provides a Celery Beat integration contract without coupling
the task kernel directly to Celery.

The actual Celery implementation should be injected by the
deployment layer.

Example:

Production:
    DatavionOS
        |
        v
    CeleryBeatAdapter
        |
        v
    Celery Beat

Development:
    DatavionOS
        |
        v
    In-memory scheduler
"""

from __future__ import annotations

from apps.common.tasks.adapters.base import (
    BaseSchedulerAdapter,
)
from apps.common.tasks.scheduler import (
    ScheduleDefinition,
)


class CeleryBeatAdapter(
    BaseSchedulerAdapter,
):
    """
    Celery Beat scheduler adapter.

    Responsible for translating DatavionOS schedule
    definitions into Celery Beat schedules.

    The Celery dependency is intentionally external.
    """

    name = "celery_beat"

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

        Translation to Celery Beat format happens
        in deployment-specific integration code.
        """

        self._schedules[definition.schedule_id] = definition

    def unregister(
        self,
        schedule_id: str,
    ) -> None:
        """
        Remove a schedule.
        """

        self._schedules.pop(
            schedule_id,
            None,
        )

    def sync(
        self,
    ) -> None:
        """
        Synchronize schedules with Celery Beat.

        Placeholder for deployment integration.

        Example:

        celery_app.conf.beat_schedule = {
            ...
        }
        """

        return


__all__: tuple[str, ...] = ("CeleryBeatAdapter",)
