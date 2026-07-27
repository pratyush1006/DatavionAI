"""
Workflow execution engine for DatavionOS.

Provides the runtime state machine responsible for:

- validating transitions
- moving workflow states
- executing workflow changes
- producing execution results

The engine is framework-level only.
"""

from __future__ import annotations

from uuid import uuid4

from apps.common.workflow.exceptions import (
    InvalidTransitionError,
    WorkflowExecutionError,
)
from apps.common.workflow.models import (
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


class WorkflowEngine:
    """
    Workflow runtime engine.

    Executes registered workflows and manages state changes.
    """

    def start(
        self,
        workflow_name: WorkflowName,
        *,
        context: MutableWorkflowContext | None = None,
    ) -> WorkflowExecution:
        """
        Start a workflow execution.
        """

        workflow = workflow_registry.get(
            workflow_name,
        )

        return WorkflowExecution(
            workflow_id=str(
                uuid4(),
            ),
            workflow_name=workflow.name,
            current_state=workflow.initial_state,
            context=context or {},
        )

    def transition(
        self,
        execution: WorkflowExecution,
        target_state: StateName,
    ) -> WorkflowExecution:
        """
        Move workflow execution to another state.
        """

        workflow = workflow_registry.get(
            execution.workflow_name,
        )

        transition = next(
            (
                item
                for item in workflow.transitions
                if (
                    item.from_state == execution.current_state
                    and item.to_state == target_state
                )
            ),
            None,
        )

        if transition is None:
            raise InvalidTransitionError(
                (
                    f"Cannot transition workflow "
                    f"'{execution.workflow_name}' "
                    f"from '{execution.current_state}' "
                    f"to '{target_state}'."
                ),
            )

        return WorkflowExecution(
            workflow_id=execution.workflow_id,
            workflow_name=execution.workflow_name,
            current_state=target_state,
            status=execution.status,
            context=execution.context,
            created_at=execution.created_at,
        )

    def complete(
        self,
        execution: WorkflowExecution,
    ) -> WorkflowExecutionResult:
        """
        Complete workflow execution.
        """

        return WorkflowExecutionResult(
            workflow_id=execution.workflow_id,
            success=True,
            current_state=execution.current_state,
            message="Workflow completed.",
            data=execution.context,
        )

    def fail(
        self,
        execution: WorkflowExecution,
        *,
        reason: str,
    ) -> WorkflowExecutionResult:
        """
        Mark workflow execution as failed.
        """

        return WorkflowExecutionResult(
            workflow_id=execution.workflow_id,
            success=False,
            current_state=execution.current_state,
            message=reason,
            data=execution.context,
        )

    def execute(
        self,
        workflow_name: WorkflowName,
        *,
        context: MutableWorkflowContext | None = None,
    ) -> WorkflowExecutionResult:
        """
        Execute a workflow.

        Starts the workflow and returns an execution result.

        Domain-specific actions can be layered on top through
        services, events, and tasks.
        """

        try:
            execution = self.start(
                workflow_name,
                context=context,
            )

            return self.complete(
                execution,
            )

        except Exception as exc:
            if isinstance(
                exc,
                WorkflowExecutionError,
            ):
                raise

            raise WorkflowExecutionError(
                str(exc),
            ) from exc


workflow_engine = WorkflowEngine()


__all__: tuple[str, ...] = (
    "WorkflowEngine",
    "workflow_engine",
)
