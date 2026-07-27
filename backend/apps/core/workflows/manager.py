"""
Workflow manager.

Central orchestration entry point for executing workflows across the
DatavionAI platform.
"""

from __future__ import annotations

import logging
from typing import Any, TypeVar

from apps.core.workflows.base import BaseWorkflow
from apps.core.workflows.context import WorkflowContext
from apps.core.workflows.result import WorkflowResult

T = TypeVar("T")

logger = logging.getLogger(__name__)


class WorkflowManager:
    """
    Enterprise workflow manager.

    Responsibilities
    ----------------
    - Workflow execution
    - Workflow registry
    - Dependency injection
    - Structured logging
    - Future retry support
    - Future metrics
    - Future tracing
    """

    def __init__(
        self,
    ) -> None:
        self._workflows: dict[
            str,
            type[BaseWorkflow[Any]],
        ] = {}

    #
    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    #

    def register(
        self,
        *,
        name: str,
        workflow: type[BaseWorkflow[Any]],
    ) -> None:
        """
        Register a workflow class.
        """

        if name in self._workflows:
            raise ValueError(
                f"Workflow '{name}' is already registered.",
            )

        self._workflows[name] = workflow

        logger.debug(
            "Workflow registered.",
            extra={
                "workflow": name,
            },
        )

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove a workflow registration.
        """

        self._workflows.pop(
            name,
            None,
        )

    def is_registered(
        self,
        name: str,
    ) -> bool:
        """
        Return whether a workflow exists.
        """

        return name in self._workflows

    def get(
        self,
        name: str,
    ) -> type[BaseWorkflow[Any]]:
        """
        Return a registered workflow class.
        """

        try:
            return self._workflows[name]
        except KeyError as exc:
            raise LookupError(
                f"Workflow '{name}' is not registered.",
            ) from exc

    def registered_workflows(
        self,
    ) -> tuple[str, ...]:
        """
        Return registered workflow names.
        """

        return tuple(
            sorted(
                self._workflows.keys(),
            ),
        )

    #
    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------
    #

    def create(
        self,
        workflow: type[BaseWorkflow[T]],
        **kwargs: Any,
    ) -> BaseWorkflow[T]:
        """
        Instantiate a workflow.

        This method exists so dependency injection can later replace
        direct construction without changing callers.
        """

        return workflow(
            **kwargs,
        )

    #
    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------
    #

    def execute(
        self,
        workflow: type[BaseWorkflow[T]],
        *,
        context: WorkflowContext,
        **kwargs: Any,
    ) -> WorkflowResult[T]:
        """
        Execute a workflow class.
        """

        logger.info(
            "Executing workflow.",
            extra={
                "workflow": workflow.__name__,
                **context.to_dict(),
            },
        )

        instance = self.create(
            workflow,
            **kwargs,
        )

        result = instance.execute(
            context=context,
        )

        logger.info(
            "Workflow execution finished.",
            extra={
                "workflow": workflow.__name__,
                "success": result.success,
                "duration_ms": result.duration_ms,
                **context.to_dict(),
            },
        )

        return result

    def run(
        self,
        name: str,
        *,
        context: WorkflowContext,
        **kwargs: Any,
    ) -> WorkflowResult[Any]:
        """
        Execute a registered workflow by name.
        """

        workflow = self.get(
            name,
        )

        return self.execute(
            workflow,
            context=context,
            **kwargs,
        )

    #
    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    #

    def clear(
        self,
    ) -> None:
        """
        Remove all registered workflows.

        Primarily intended for testing.
        """

        self._workflows.clear()

    def __contains__(
        self,
        name: object,
    ) -> bool:
        """
        Support the ``in`` operator.
        """

        return isinstance(name, str) and self.is_registered(name)

    def __len__(
        self,
    ) -> int:
        """
        Return the number of registered workflows.
        """

        return len(self._workflows)

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return f"{self.__class__.__name__}(registered={len(self)})"


workflow_manager = WorkflowManager()


__all__: tuple[str, ...] = (
    "WorkflowManager",
    "workflow_manager",
)
