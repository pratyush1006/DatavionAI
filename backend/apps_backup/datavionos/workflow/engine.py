"""
Workflow engine contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.workflow.execution import (
    WorkflowExecutionContext,
    WorkflowExecutionResult,
)
from apps.datavionos.workflow.instance import (
    WorkflowInstance,
)


@runtime_checkable
class WorkflowEngine(
    Protocol,
):
    """
    Orchestrates workflow execution.
    """

    async def start(
        self,
        workflow_id: str,
        context: WorkflowExecutionContext,
    ) -> WorkflowExecutionResult:
        """
        Start a new workflow.
        """

    async def execute(
        self,
        instance: WorkflowInstance,
        context: WorkflowExecutionContext,
    ) -> WorkflowExecutionResult:
        """
        Execute the next workflow step.
        """

    async def resume(
        self,
        instance: WorkflowInstance,
        context: WorkflowExecutionContext,
    ) -> WorkflowExecutionResult:
        """
        Resume a paused workflow.
        """

    async def cancel(
        self,
        instance: WorkflowInstance,
    ) -> None:
        """
        Cancel a workflow instance.
        """

    async def restart(
        self,
        instance: WorkflowInstance,
        context: WorkflowExecutionContext,
    ) -> WorkflowExecutionResult:
        """
        Restart a workflow instance.
        """

    async def is_running(
        self,
        instance_id: str,
    ) -> bool:
        """
        Determine whether a workflow
        instance is currently running.
        """


__all__ = [
    "WorkflowEngine",
]
