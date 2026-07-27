"""
Task scheduler abstraction for DatavionOS.

Provides scheduling contracts for recurring and delayed tasks.

This framework layer does not depend on any scheduler engine.

Future adapters:

- Celery Beat
- APScheduler
- Cloud Scheduler
- Kubernetes CronJobs
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from uuid import uuid4

from apps.common.tasks.constants import (
    DEFAULT_QUEUE,
)
from apps.common.tasks.types import (
    TaskName,
    TaskPayload,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ScheduleDefinition:
    """
    Defines a scheduled task.

    Supports:

    - recurring execution
    - delayed execution
    - multi-tenant scheduling
    - scheduler adapters
    """

    task_name: TaskName

    schedule: str

    schedule_id: str = field(
        default_factory=lambda: str(uuid4()),
    )

    queue: str = DEFAULT_QUEUE

    payload: TaskPayload = field(
        default_factory=dict,
    )

    timezone: str = "UTC"

    enabled: bool = True


class TaskScheduler:
    """
    Task scheduler registry.

    Stores scheduling definitions and exposes them
    to scheduler adapters.
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize scheduler registry.
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
        Register scheduled task.
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

    def get(
        self,
        schedule_id: str,
    ) -> ScheduleDefinition | None:
        """
        Return schedule definition.
        """

        return self._schedules.get(
            schedule_id,
        )

    def all(
        self,
    ) -> tuple[ScheduleDefinition, ...]:
        """
        Return all registered schedules.
        """

        return tuple(
            self._schedules.values(),
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all schedules.
        """

        self._schedules.clear()


task_scheduler = TaskScheduler()


__all__: tuple[str, ...] = (
    "ScheduleDefinition",
    "TaskScheduler",
    "task_scheduler",
)
