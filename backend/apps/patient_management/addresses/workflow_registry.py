"""
Patient Address workflow registration.
"""

from __future__ import annotations

from apps.core.workflows import (
    workflow_registry,
)
from apps.patient_management.addresses.workflows import (
    AddressActivationWorkflow,
    AddressCreationWorkflow,
    AddressDeactivationWorkflow,
    AddressDeletionWorkflow,
    AddressPrimaryWorkflow,
    AddressUpdateWorkflow,
    AddressVerificationWorkflow,
)


def register_address_workflows() -> None:
    """
    Register all canonical Patient Address workflows.
    """
    workflows = {
        "address.create": AddressCreationWorkflow,
        "address.update": AddressUpdateWorkflow,
        "address.verify": AddressVerificationWorkflow,
        "address.activate": AddressActivationWorkflow,
        "address.deactivate": AddressDeactivationWorkflow,
        "address.set_primary": AddressPrimaryWorkflow,
        "address.delete": AddressDeletionWorkflow,
    }

    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(
            name,
        ):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("register_address_workflows",)
