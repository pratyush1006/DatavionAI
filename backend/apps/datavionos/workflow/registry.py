"""
Workflow registry contracts.
"""

from __future__ import annotations

from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.workflow.definition import (
    WorkflowDefinition,
)
from apps.datavionos.workflow.descriptor import (
    WorkflowCategory,
)


@runtime_checkable
class WorkflowRegistry(
    Protocol,
):
    """
    Registry of available workflow definitions.
    """

    async def register(
        self,
        definition: WorkflowDefinition,
    ) -> None:
        """
        Register a workflow definition.
        """

    async def unregister(
        self,
        workflow_id: str,
    ) -> None:
        """
        Remove a workflow definition.
        """

    async def get(
        self,
        workflow_id: str,
    ) -> WorkflowDefinition | None:
        """
        Return a workflow definition.
        """

    async def contains(
        self,
        workflow_id: str,
    ) -> bool:
        """
        Determine whether a workflow
        is registered.
        """

    async def list(
        self,
    ) -> tuple[WorkflowDefinition, ...]:
        """
        Return all registered workflows.
        """

    async def list_by_category(
        self,
        category: WorkflowCategory,
    ) -> tuple[WorkflowDefinition, ...]:
        """
        Return workflow definitions
        belonging to the specified category.
        """


__all__ = [
    "WorkflowRegistry",
]
