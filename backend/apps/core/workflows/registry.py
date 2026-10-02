"""
Workflow registry.

Provides centralized registration and discovery of workflows across
the DatavionAI platform.
"""

from __future__ import annotations

import logging
from threading import RLock
from typing import Any

from apps.core.workflows.base import BaseWorkflow

logger = logging.getLogger(__name__)


class WorkflowRegistry:
    """
    Central workflow registry.

    Responsibilities

    - Register workflows
    - Remove workflows
    - Discover workflows
    - Prevent duplicate registrations
    - Thread-safe access
    """

    def __init__(
        self,
    ) -> None:
        self._lock = RLock()

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
        Register a workflow.
        """

        with self._lock:
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

        with self._lock:
            self._workflows.pop(
                name,
                None,
            )

    def clear(
        self,
    ) -> None:
        """
        Remove every registered workflow.
        """

        with self._lock:
            self._workflows.clear()

    #
    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------
    #

    def is_registered(
        self,
        name: str,
    ) -> bool:
        """
        Determine whether a workflow exists.
        """

        with self._lock:
            return name in self._workflows

    def get(
        self,
        name: str,
    ) -> type[BaseWorkflow[Any]]:
        """
        Return a registered workflow.
        """

        with self._lock:
            try:
                return self._workflows[name]
            except KeyError as exc:
                raise LookupError(
                    f"Workflow '{name}' is not registered.",
                ) from exc

    #
    # ------------------------------------------------------------------
    # Enumeration
    # ------------------------------------------------------------------
    #

    def names(
        self,
    ) -> tuple[str, ...]:
        """
        Return all registered workflow names.
        """

        with self._lock:
            return tuple(
                sorted(
                    self._workflows.keys(),
                ),
            )

    def all(
        self,
    ) -> dict[str, type[BaseWorkflow[Any]]]:
        """
        Return a shallow copy of the workflow registry.
        """

        with self._lock:
            return dict(
                self._workflows,
            )

    def items(
        self,
    ) -> tuple[
        tuple[
            str,
            type[BaseWorkflow[Any]],
        ],
        ...,
    ]:
        """
        Return all registered workflow entries.
        """

        with self._lock:
            return tuple(
                sorted(
                    self._workflows.items(),
                    key=lambda item: item[0],
                ),
            )

    #
    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------
    #

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

        with self._lock:
            return len(
                self._workflows,
            )

    def __iter__(
        self,
    ):
        """
        Iterate over registered workflow names.
        """

        return iter(
            self.names(),
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return f"{self.__class__.__name__}(registered={len(self)})"


workflow_registry = WorkflowRegistry()


__all__: tuple[str, ...] = (
    "WorkflowRegistry",
    "workflow_registry",
)
