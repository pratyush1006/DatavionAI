"""
Patient Portal workflow registry integration.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.portal.workflows import (
    PatientPortalCreationWorkflow,
    PatientPortalDeletionWorkflow,
    PatientPortalInvitationWorkflow,
    PatientPortalLifecycleWorkflow,
    PatientPortalRestoreWorkflow,
    PatientPortalUpdateWorkflow,
)


def register_workflows() -> None:
    """Register all Patient Portal workflows idempotently."""

    registrations = (
        (
            "patient_portal.create",
            PatientPortalCreationWorkflow,
        ),
        (
            "patient_portal.update",
            PatientPortalUpdateWorkflow,
        ),
        (
            "patient_portal.delete",
            PatientPortalDeletionWorkflow,
        ),
        (
            "patient_portal.restore",
            PatientPortalRestoreWorkflow,
        ),
        (
            "patient_portal.lifecycle",
            PatientPortalLifecycleWorkflow,
        ),
        (
            "patient_portal.invite",
            PatientPortalInvitationWorkflow,
        ),
    )

    for name, workflow in registrations:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


register_workflows()

__all__ = ("register_workflows",)
