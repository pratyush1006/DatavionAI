"""
Task runner for DatavionOS.

Provides the execution layer between registered tasks and the
task framework.

This layer is queue-engine independent.

Future adapters:

- Celery
- Django-Q
- Azure Service Bus
- AWS SQS
- RabbitMQ
"""

from __future__ import annotations

from apps.common.tasks.base import (
    TaskContext,
)
from apps.common.tasks.exceptions import (
    TaskExecutionError,
)
from apps.common.tasks.registry import (
    task_registry,
)
from apps.common.tasks.types import (
    TaskName,
    TaskPayload,
    TaskResult,
)


class TaskRunner:
    """
    Executes registered tasks.

    Execution flow:

        Task Name
            |
            v
        Registry lookup
            |
            v
        Task instance
            |
            v
        Context creation
            |
            v
        Execute payload
    """

    def run(
        self,
        name: TaskName,
        payload: TaskPayload | None = None,
        *,
        context: TaskContext | None = None,
    ) -> TaskResult:
        """
        Execute a registered task.

        Args:
            name:
                Registered task name.

            payload:
                Task input payload.

            context:
                Runtime execution context.

        Returns:
            Task execution result.
        """

        try:
            task = task_registry.create(
                name,
            )

            return task.run(
                payload or {},
                context=context,
            )

        except TaskExecutionError:
            raise

        except Exception as exc:
            raise TaskExecutionError(
                str(exc),
            ) from exc


task_runner = TaskRunner()


def execute_task(
    name: TaskName,
    payload: TaskPayload | None = None,
    *,
    context: TaskContext | None = None,
) -> TaskResult:
    """
    Convenience function for executing tasks.
    """

    return task_runner.run(
        name,
        payload,
        context=context,
    )


__all__: tuple[str, ...] = (
    "TaskRunner",
    "execute_task",
    "task_runner",
)
