"""
Workflow descriptor contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class WorkflowCategory(
    StrEnum,
):
    """
    Workflow classification.
    """

    CLINICAL = "clinical"

    ADMINISTRATIVE = "administrative"

    FINANCIAL = "financial"

    LABORATORY = "laboratory"

    PHARMACY = "pharmacy"

    AI = "ai"

    SYSTEM = "system"


class WorkflowStatus(
    StrEnum,
):
    """
    Workflow status.
    """

    DRAFT = "draft"

    ACTIVE = "active"

    DEPRECATED = "deprecated"

    DISABLED = "disabled"


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowDescriptor:
    """
    Workflow metadata.
    """

    id: str

    name: str

    version: str

    category: WorkflowCategory

    status: WorkflowStatus = WorkflowStatus.DRAFT

    description: str | None = None


__all__ = [
    "WorkflowCategory",
    "WorkflowDescriptor",
    "WorkflowStatus",
]
