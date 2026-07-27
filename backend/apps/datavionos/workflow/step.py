"""
Workflow step contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class WorkflowStepType(
    StrEnum,
):
    """
    Supported workflow step types.
    """

    START = "start"

    TASK = "task"

    DECISION = "decision"

    APPROVAL = "approval"

    AI = "ai"

    EVENT = "event"

    END = "end"


class WorkflowStepStatus(
    StrEnum,
):
    """
    Runtime status of a workflow step.
    """

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    SKIPPED = "skipped"

    FAILED = "failed"

    CANCELLED = "cancelled"


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowStep:
    """
    Immutable workflow step definition.
    """

    id: str

    name: str

    type: WorkflowStepType

    description: str | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class WorkflowStepExecutor(
    Protocol,
):
    """
    Executes a workflow step.
    """

    async def execute(
        self,
        step: WorkflowStep,
    ) -> WorkflowStepStatus:
        """
        Execute the workflow step.
        """


__all__ = [
    "WorkflowStep",
    "WorkflowStepExecutor",
    "WorkflowStepStatus",
    "WorkflowStepType",
]
