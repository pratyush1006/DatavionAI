"""
DatavionOS SaaS Billing workflow registry.

Stores and resolves workflow classes.
"""

from __future__ import annotations

from .base import (
    BaseWorkflow,
)


class WorkflowRegistry:
    """
    Enterprise workflow registry.
    """

    _workflows: dict[
        str,
        type[BaseWorkflow],
    ] = {}

    @classmethod
    def register(
        cls,
        name: str,
        workflow: type[BaseWorkflow],
    ) -> None:
        """
        Register workflow.
        """

        cls._workflows[name] = workflow

    @classmethod
    def get(
        cls,
        name: str,
    ) -> type[BaseWorkflow]:
        """
        Retrieve workflow.
        """

        workflow = cls._workflows.get(
            name,
        )

        if workflow is None:
            raise KeyError(f"Workflow '{name}' not registered.")

        return workflow

    @classmethod
    def execute(
        cls,
        name: str,
        *args,
        **kwargs,
    ):
        """
        Execute workflow.
        """

        workflow = cls.get(
            name,
        )

        return workflow().execute(
            *args,
            **kwargs,
        )

    @classmethod
    def all(
        cls,
    ) -> dict:
        """
        Return registered workflows.
        """

        return dict(
            cls._workflows,
        )


__all__ = [
    "WorkflowRegistry",
]
