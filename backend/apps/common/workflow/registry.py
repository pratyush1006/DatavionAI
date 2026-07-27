"""
Workflow registry for DatavionOS.

Maintains registered workflow definitions and provides lookup
capabilities for the workflow engine.

The registry is infrastructure-level only.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.common.workflow.exceptions import (
    WorkflowAlreadyRegisteredError,
    WorkflowNotFoundError,
)
from apps.common.workflow.models import (
    Workflow,
)
from apps.common.workflow.types import (
    WorkflowName,
)


class WorkflowRegistry:
    """
    Central workflow registry.

    Supports:

    - Workflow registration
    - Workflow lookup
    - Workflow discovery
    - Duplicate protection
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize registry.
        """

        self._workflows: dict[
            WorkflowName,
            Workflow,
        ] = {}

    def register(
        self,
        workflow: Workflow,
    ) -> None:
        """
        Register a workflow definition.

        Raises:
            WorkflowAlreadyRegisteredError:
                If workflow already exists.
        """

        if workflow.name in self._workflows:
            raise WorkflowAlreadyRegisteredError(
                (f"Workflow '{workflow.name}' is already registered."),
            )

        self._workflows[workflow.name] = workflow

    def unregister(
        self,
        name: WorkflowName,
    ) -> None:
        """
        Remove workflow registration.
        """

        self._workflows.pop(
            name,
            None,
        )

    def get(
        self,
        name: WorkflowName,
    ) -> Workflow:
        """
        Return a workflow definition.

        Raises:
            WorkflowNotFoundError:
                If workflow does not exist.
        """

        workflow = self._workflows.get(
            name,
        )

        if workflow is None:
            raise WorkflowNotFoundError(
                (f"Workflow '{name}' does not exist."),
            )

        return workflow

    def has(
        self,
        name: WorkflowName,
    ) -> bool:
        """
        Check whether a workflow exists.
        """

        return name in self._workflows

    def all(
        self,
    ) -> Iterable[Workflow]:
        """
        Return all registered workflows.
        """

        return self._workflows.values()

    def clear(
        self,
    ) -> None:
        """
        Remove all workflows.
        """

        self._workflows.clear()


workflow_registry = WorkflowRegistry()


__all__: tuple[str, ...] = (
    "WorkflowRegistry",
    "workflow_registry",
)
