"""
Task registry for DatavionOS.

Maintains registered task definitions and provides lookup
capabilities for the task execution framework.

The registry is infrastructure-level only.

Business modules register their own tasks.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.common.tasks.base import (
    BaseTask,
)
from apps.common.tasks.exceptions import (
    TaskAlreadyRegisteredError,
    TaskNotRegisteredError,
)
from apps.common.tasks.types import (
    TaskName,
)


class TaskRegistry:
    """
    Central task registry.

    Supports:

    - Task registration
    - Task lookup
    - Task discovery
    - Task creation
    - Duplicate protection
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize registry.
        """

        self._tasks: dict[
            TaskName,
            type[BaseTask],
        ] = {}

    def register(
        self,
        task: type[BaseTask],
    ) -> None:
        """
        Register a task class.
        """

        if not issubclass(
            task,
            BaseTask,
        ):
            raise TypeError(
                "Registered task must inherit BaseTask.",
            )

        if not task.name:
            raise ValueError(
                "Task name cannot be empty.",
            )

        if task.name in self._tasks:
            raise TaskAlreadyRegisteredError(
                (f"Task '{task.name}' is already registered."),
            )

        self._tasks[task.name] = task

    def unregister(
        self,
        name: TaskName,
    ) -> None:
        """
        Remove task registration.
        """

        self._tasks.pop(
            name,
            None,
        )

    def get(
        self,
        name: TaskName,
    ) -> type[BaseTask]:
        """
        Return registered task class.
        """

        task = self._tasks.get(
            name,
        )

        if task is None:
            raise TaskNotRegisteredError(
                (f"Task '{name}' is not registered."),
            )

        return task

    def create(
        self,
        name: TaskName,
    ) -> BaseTask:
        """
        Create task instance.
        """

        task_class = self.get(
            name,
        )

        return task_class()

    def has(
        self,
        name: TaskName,
    ) -> bool:
        """
        Check task availability.
        """

        return name in self._tasks

    def clear(
        self,
    ) -> None:
        """
        Remove all tasks.
        """

        self._tasks.clear()

    def tasks(
        self,
    ) -> Iterable[TaskName]:
        """
        Return registered task names.
        """

        return self._tasks.keys()


task_registry = TaskRegistry()


__all__: tuple[str, ...] = (
    "TaskRegistry",
    "task_registry",
)
