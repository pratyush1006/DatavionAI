"""
Patient Contact workflow registration.

Registers all canonical Contact workflows into the shared DatavionOS
workflow registry.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.contacts.workflows import (
    ContactActivationWorkflow,
    ContactCreationWorkflow,
    ContactDeactivationWorkflow,
    ContactDeletionWorkflow,
    ContactPrimaryWorkflow,
    ContactUpdateWorkflow,
    ContactVerificationWorkflow,
)


def register_contact_workflows() -> None:
    """
    Register all canonical Patient Contact workflows.

    Registration is idempotent so Django application startup can safely
    invoke this function more than once.
    """
    workflows = {
        "contact.create": ContactCreationWorkflow,
        "contact.update": ContactUpdateWorkflow,
        "contact.verify": ContactVerificationWorkflow,
        "contact.activate": ContactActivationWorkflow,
        "contact.deactivate": ContactDeactivationWorkflow,
        "contact.set_primary": ContactPrimaryWorkflow,
        "contact.delete": ContactDeletionWorkflow,
    }

    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(
            name,
        ):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("register_contact_workflows",)
