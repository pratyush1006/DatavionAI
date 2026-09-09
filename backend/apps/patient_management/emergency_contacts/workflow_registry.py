"""
Emergency Contacts workflow registration.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.emergency_contacts.workflows import (
    EmergencyContactActivationWorkflow,
    EmergencyContactBlockWorkflow,
    EmergencyContactCreationWorkflow,
    EmergencyContactDeactivationWorkflow,
    EmergencyContactDeletionWorkflow,
    EmergencyContactPrimaryWorkflow,
    EmergencyContactUpdateWorkflow,
    EmergencyContactVerificationWorkflow,
)


def register_emergency_contact_workflows() -> None:
    """
    Register all Emergency Contact workflows.
    """

    workflows = {
        "emergency_contact.create": (EmergencyContactCreationWorkflow),
        "emergency_contact.update": (EmergencyContactUpdateWorkflow),
        "emergency_contact.delete": (EmergencyContactDeletionWorkflow),
        "emergency_contact.verify": (EmergencyContactVerificationWorkflow),
        "emergency_contact.activate": (EmergencyContactActivationWorkflow),
        "emergency_contact.deactivate": (EmergencyContactDeactivationWorkflow),
        "emergency_contact.block": (EmergencyContactBlockWorkflow),
        "emergency_contact.set_primary": (EmergencyContactPrimaryWorkflow),
    }

    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(
            name,
        ):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("register_emergency_contact_workflows",)
