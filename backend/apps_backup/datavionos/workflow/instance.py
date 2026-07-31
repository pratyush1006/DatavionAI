"""
Workflow instance contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import (
    UTC,
    datetime,
)
from enum import StrEnum


class WorkflowInstanceStatus(
    StrEnum,
):
    """
    Runtime status of a workflow instance.
    """

    CREATED = "created"

    RUNNING = "running"

    WAITING = "waiting"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowInstance:
    """
    Represents a single execution of a workflow.
    """

    id: str

    workflow_id: str

    version: str

    current_step: str

    status: WorkflowInstanceStatus = WorkflowInstanceStatus.CREATED

    created_at: datetime = datetime.now(UTC)


__all__ = [
    "WorkflowInstance",
    "WorkflowInstanceStatus",
]
