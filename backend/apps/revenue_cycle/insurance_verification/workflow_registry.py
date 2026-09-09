"""Revenue Cycle Insurance Verification workflow registration."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.revenue_cycle.insurance_verification.workflows import (
    InsuranceVerificationCreationWorkflow,
    InsuranceVerificationDeletionWorkflow,
    InsuranceVerificationLifecycleWorkflow,
    InsuranceVerificationRestoreWorkflow,
    InsuranceVerificationUpdateWorkflow,
)

WORKFLOW_DEFINITIONS = (
    (
        "revenue_cycle.insurance_verification.create",
        InsuranceVerificationCreationWorkflow,
    ),
    (
        "revenue_cycle.insurance_verification.update",
        InsuranceVerificationUpdateWorkflow,
    ),
    (
        "revenue_cycle.insurance_verification.delete",
        InsuranceVerificationDeletionWorkflow,
    ),
    (
        "revenue_cycle.insurance_verification.restore",
        InsuranceVerificationRestoreWorkflow,
    ),
    (
        "revenue_cycle.insurance_verification.lifecycle",
        InsuranceVerificationLifecycleWorkflow,
    ),
)


def register_workflows() -> None:
    """Register Insurance Verification workflows idempotently."""

    for name, workflow in WORKFLOW_DEFINITIONS:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


register_workflows()

__all__ = ("WORKFLOW_DEFINITIONS", "register_workflows")
