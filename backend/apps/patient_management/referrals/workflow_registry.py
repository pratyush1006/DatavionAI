"""
Workflow registry integration for Patient Referrals.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.referrals.workflows import (
    ReferralCreationWorkflow,
    ReferralDeletionWorkflow,
    ReferralLifecycleWorkflow,
    ReferralRestoreWorkflow,
    ReferralUpdateWorkflow,
)


def register_workflows() -> None:
    """Register all Patient Referral workflows."""

    registrations = (
        ("patient_referral.create", ReferralCreationWorkflow),
        ("patient_referral.update", ReferralUpdateWorkflow),
        ("patient_referral.delete", ReferralDeletionWorkflow),
        ("patient_referral.restore", ReferralRestoreWorkflow),
        ("patient_referral.lifecycle", ReferralLifecycleWorkflow),
    )

    for name, workflow in registrations:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


register_workflows()


__all__ = ("register_workflows",)
