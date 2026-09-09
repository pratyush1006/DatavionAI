from __future__ import annotations

"""Workflow registry integration for Revenue Cycle Coding."""

from apps.core.workflows import workflow_registry

from .workflows import CodingWorkflow


def register_coding_workflows() -> None:
    """Register the Coding workflow once."""

    name = "revenue_cycle.coding"

    if not workflow_registry.is_registered(name):
        workflow_registry.register(
            name=name,
            workflow=CodingWorkflow,
        )


__all__ = ("register_coding_workflows",)
