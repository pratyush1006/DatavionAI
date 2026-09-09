"""Revenue Cycle Eligibility workflow registration."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.revenue_cycle.eligibility.workflows import (
    EligibilityCreationWorkflow,
    EligibilityDeletionWorkflow,
    EligibilityLifecycleWorkflow,
    EligibilityRestoreWorkflow,
    EligibilityUpdateWorkflow,
)


def register_workflows() -> None:
    """Register Eligibility workflows idempotently."""
    for name, workflow in (
        ("revenue_cycle.eligibility.create", EligibilityCreationWorkflow),
        ("revenue_cycle.eligibility.update", EligibilityUpdateWorkflow),
        ("revenue_cycle.eligibility.delete", EligibilityDeletionWorkflow),
        ("revenue_cycle.eligibility.restore", EligibilityRestoreWorkflow),
        ("revenue_cycle.eligibility.lifecycle", EligibilityLifecycleWorkflow),
    ):
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


register_workflows()
__all__ = ("register_workflows",)
