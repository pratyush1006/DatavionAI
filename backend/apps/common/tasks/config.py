"""
Task configuration models for DatavionOS.

Defines immutable runtime configuration for task execution
and scheduling.

Queue providers remain abstract.
Compatible with:

- Celery
- Redis Queue
- Background workers
- Custom runners
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.tasks.constants import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_QUEUE,
    DEFAULT_RETRY_DELAY,
    DEFAULT_TASK_TIMEOUT,
)


@dataclass(
    frozen=True,
    slots=True,
)
class TaskConfiguration:
    """
    Task execution configuration.
    """

    timeout: int = DEFAULT_TASK_TIMEOUT

    max_retries: int = DEFAULT_MAX_RETRIES

    retry_delay: int = DEFAULT_RETRY_DELAY

    retry_enabled: bool = True

    queue: str = DEFAULT_QUEUE

    priority: str = "normal"

    idempotent: bool = True


@dataclass(
    frozen=True,
    slots=True,
)
class SchedulerConfiguration:
    """
    Scheduled task configuration.
    """

    enabled: bool = True

    timezone: str = "UTC"

    max_concurrent_tasks: int = 10

    polling_interval_seconds: int = 30


DEFAULT_TASK_CONFIGURATION = TaskConfiguration()


DEFAULT_SCHEDULER_CONFIGURATION = SchedulerConfiguration()


__all__: tuple[str, ...] = (
    "DEFAULT_SCHEDULER_CONFIGURATION",
    "DEFAULT_TASK_CONFIGURATION",
    "SchedulerConfiguration",
    "TaskConfiguration",
)
