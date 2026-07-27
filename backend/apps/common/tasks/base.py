"""
Base task abstractions for DatavionOS.

Defines the framework-level task contract.

Business applications should implement concrete tasks in their
own modules and inherit from this base class.

The task framework is tenant-aware and queue-provider
independent.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from uuid import uuid4

from apps.common.tasks.config import (
    DEFAULT_TASK_CONFIGURATION,
    TaskConfiguration,
)
from apps.common.tasks.constants import (
    TASK_PENDING,
)
from apps.common.tasks.types import (
    TaskID,
    TaskName,
    TaskPayload,
    TaskResult,
    TaskStatus,
)


@dataclass(
    frozen=True,
    slots=True,
)
class TaskContext:
    """
    Runtime context for task execution.

    Preserves execution metadata across:

    - API requests
    - background workers
    - scheduled tasks
    - event-triggered execution

    No queue implementation details are stored here.
    """

    task_id: TaskID = field(
        default_factory=lambda: str(uuid4()),
    )

    status: TaskStatus = TASK_PENDING

    tenant_id: str | None = None

    organization_id: str | None = None

    user_id: str | None = None

    request_id: str | None = None

    correlation_id: str | None = None

    metadata: dict[str, object] = field(
        default_factory=dict,
    )


class BaseTask(
    ABC,
):
    """
    Base DatavionOS task.

    Provides:

    - task identity
    - configuration
    - execution context
    - lifecycle hooks
    - execution contract
    """

    name: TaskName = ""

    configuration: TaskConfiguration = DEFAULT_TASK_CONFIGURATION

    def before_execute(
        self,
        context: TaskContext,
    ) -> None:
        """
        Hook executed before task execution.
        """

    def after_execute(
        self,
        context: TaskContext,
        result: TaskResult,
    ) -> None:
        """
        Hook executed after successful execution.
        """

    def on_failure(
        self,
        context: TaskContext,
        exception: Exception,
    ) -> None:
        """
        Hook executed when task execution fails.
        """

    @abstractmethod
    def execute(
        self,
        payload: TaskPayload,
    ) -> TaskResult:
        """
        Execute task business logic.

        Domain applications implement this method.
        """

    def run(
        self,
        payload: TaskPayload,
        *,
        context: TaskContext | None = None,
    ) -> TaskResult:
        """
        Execute complete task lifecycle.

        Context can be supplied by:

        - API layer
        - scheduler
        - event dispatcher
        - task runner
        """

        execution_context = context if context is not None else TaskContext()

        try:
            self.before_execute(
                execution_context,
            )

            result = self.execute(
                payload,
            )

            self.after_execute(
                execution_context,
                result,
            )

            return result

        except Exception as exc:
            self.on_failure(
                execution_context,
                exc,
            )

            raise


__all__: tuple[str, ...] = (
    "BaseTask",
    "TaskContext",
)
