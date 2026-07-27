"""
Workflow transition contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class WorkflowTransitionType(
    StrEnum,
):
    """
    Supported workflow transition types.
    """

    DEFAULT = "default"

    CONDITIONAL = "conditional"

    PARALLEL = "parallel"

    EVENT = "event"

    MANUAL = "manual"


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowTransition:
    """
    Immutable workflow transition.
    """

    id: str

    source_step: str

    target_step: str

    type: WorkflowTransitionType = WorkflowTransitionType.DEFAULT

    condition: str | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class WorkflowTransitionEvaluator(
    Protocol,
):
    """
    Evaluates workflow transitions.
    """

    async def evaluate(
        self,
        transition: WorkflowTransition,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Determine whether the transition
        may be taken.
        """


__all__ = [
    "WorkflowTransition",
    "WorkflowTransitionEvaluator",
    "WorkflowTransitionType",
]
