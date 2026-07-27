"""
Workflow services for DatavionOS.

Provides the application service layer for workflow management.

Business applications should use this service layer instead of
directly accessing the workflow registry or engine.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.common.workflow.engine import (
    workflow_engine,
)
from apps.common.workflow.models import (
    Workflow,
    WorkflowExecution,
    WorkflowExecutionResult,
)
from apps.common.workflow.registry import (
    workflow_registry,
)
from apps.common.workflow.types import (
    MutableWorkflowContext,
    StateName,
    WorkflowName,
)


class WorkflowService:
    """
    Workflow application service.

    Provides:

    - Workflow registration
    - Workflow discovery
    - Workflow execution
    - State transitions
    """

    def register(
        self,
        workflow: Workflow,
    ) -> None:
        """
        Register a workflow definition.
        """

        workflow_registry.register(
            workflow,
        )

    def unregister(
        self,
        name: WorkflowName,
    ) -> None:
        """
        Remove workflow definition.
        """

        workflow_registry.unregister(
            name,
        )

    def get(
        self,
        name: WorkflowName,
    ) -> Workflow:
        """
        Return workflow definition.
        """

        return workflow_registry.get(
            name,
        )

    def all(
        self,
    ) -> Iterable[Workflow]:
        """
        Return all workflows.
        """

        return workflow_registry.all()

    def start(
        self,
        name: WorkflowName,
        *,
        context: MutableWorkflowContext | None = None,
    ) -> WorkflowExecution:
        """
        Start workflow execution.
        """

        return workflow_engine.start(
            name,
            context=context,
        )

    def transition(
        self,
        execution: WorkflowExecution,
        target_state: StateName,
    ) -> WorkflowExecution:
        """
        Move workflow to another state.
        """

        return workflow_engine.transition(
            execution,
            target_state,
        )

    def execute(
        self,
        name: WorkflowName,
        *,
        context: MutableWorkflowContext | None = None,
    ) -> WorkflowExecutionResult:
        """
        Execute workflow.
        """

        return workflow_engine.execute(
            name,
            context=context,
        )


workflow_service = WorkflowService()


__all__: tuple[str, ...] = (
    "WorkflowService",
    "workflow_service",
)
