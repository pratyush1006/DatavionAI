"""
Workflow definition contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.workflow.descriptor import (
    WorkflowDescriptor,
)


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowDefinition:
    """
    Immutable workflow definition.
    """

    descriptor: WorkflowDescriptor

    initial_step: str

    steps: tuple[str, ...]

    transitions: tuple[str, ...] = ()


@runtime_checkable
class WorkflowProvider(
    Protocol,
):
    """
    Provides workflow definitions.
    """

    async def get_definition(
        self,
        workflow_id: str,
    ) -> WorkflowDefinition | None:
        """
        Return a workflow definition.
        """

    async def list_definitions(
        self,
    ) -> tuple[WorkflowDefinition, ...]:
        """
        Return all workflow definitions.
        """


__all__ = [
    "WorkflowDefinition",
    "WorkflowProvider",
]
