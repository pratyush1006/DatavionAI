"""
Workflow models for DatavionOS.

Defines immutable framework-level workflow models.

These models describe workflow mechanics only.

Business workflows belong to domain applications:

- patients
- laboratories
- billing
- clinical
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

from apps.common.workflow.constants import (
    DEFAULT_STATE_TYPE,
    DEFAULT_WORKFLOW_STATUS,
)
from apps.common.workflow.types import (
    StateName,
    TransitionName,
    WorkflowContext,
    WorkflowID,
    WorkflowName,
)


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowState:
    """
    Represents a workflow state.
    """

    name: StateName

    state_type: str = DEFAULT_STATE_TYPE

    description: str = ""


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowTransition:
    """
    Represents a state transition.

    Example:

        pending -> approved
    """

    name: TransitionName

    from_state: StateName

    to_state: StateName

    description: str = ""

    event_name: str | None = None


@dataclass(
    frozen=True,
    slots=True,
)
class Workflow:
    """
    Workflow definition.

    Contains states and transitions.
    """

    name: WorkflowName

    states: tuple[WorkflowState, ...]

    transitions: tuple[WorkflowTransition, ...]

    initial_state: StateName

    description: str = ""

    metadata: WorkflowContext = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowExecution:
    """
    Runtime workflow execution instance.
    """

    workflow_id: WorkflowID

    workflow_name: WorkflowName

    current_state: StateName

    status: str = DEFAULT_WORKFLOW_STATUS

    context: WorkflowContext = field(
        default_factory=dict,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowExecutionResult:
    """
    Result returned after workflow execution.
    """

    workflow_id: WorkflowID

    success: bool

    current_state: StateName

    message: str = ""

    data: WorkflowContext = field(
        default_factory=dict,
    )


__all__: tuple[str, ...] = (
    "Workflow",
    "WorkflowExecution",
    "WorkflowExecutionResult",
    "WorkflowState",
    "WorkflowTransition",
)
