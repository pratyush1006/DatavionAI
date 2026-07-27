"""
Workflow execution contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    UTC,
    datetime,
)
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)

from apps.datavionos.workflow.instance import (
    WorkflowInstance,
)


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowExecutionContext:
    """
    Runtime execution context.
    """

    variables: dict[str, Any] = field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowExecutionResult:
    """
    Result of workflow execution.
    """

    success: bool

    current_step: str

    completed: bool = False

    outputs: dict[str, Any] = field(
        default_factory=dict,
    )

    error: str | None = None

    finished_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )


@runtime_checkable
class WorkflowExecutor(
    Protocol,
):
    """
    Executes workflow instances.
    """

    async def execute(
        self,
        instance: WorkflowInstance,
        context: WorkflowExecutionContext,
    ) -> WorkflowExecutionResult:
        """
        Execute a workflow instance.
        """

    async def resume(
        self,
        instance: WorkflowInstance,
        context: WorkflowExecutionContext,
    ) -> WorkflowExecutionResult:
        """
        Resume execution of a workflow instance.
        """

    async def cancel(
        self,
        instance: WorkflowInstance,
    ) -> None:
        """
        Cancel a workflow instance.
        """


__all__ = [
    "WorkflowExecutionContext",
    "WorkflowExecutionResult",
    "WorkflowExecutor",
]
