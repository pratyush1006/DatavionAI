"""
Workflow registry for Patient Consents.
"""

from __future__ import annotations

from apps.core.workflows import (
    workflow_registry,
)
from apps.patient_management.consents.workflows import (
    PatientConsentCreationWorkflow,
    PatientConsentDeletionWorkflow,
    PatientConsentGrantWorkflow,
    PatientConsentRestoreWorkflow,
    PatientConsentRevokeWorkflow,
    PatientConsentUpdateWorkflow,
)


def register_workflows() -> None:
    """
    Register all Patient Consent workflows.
    """
    registrations = {
        "consent.create": PatientConsentCreationWorkflow,
        "consent.update": PatientConsentUpdateWorkflow,
        "consent.delete": PatientConsentDeletionWorkflow,
        "consent.restore": PatientConsentRestoreWorkflow,
        "consent.grant": PatientConsentGrantWorkflow,
        "consent.revoke": PatientConsentRevokeWorkflow,
    }

    for name, workflow in registrations.items():
        if not workflow_registry.is_registered(
            name,
        ):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("register_workflows",)
