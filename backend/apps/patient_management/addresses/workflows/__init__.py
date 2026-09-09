"""
Patient Address workflows.
"""

from apps.patient_management.addresses.workflows.address_creation import (
    AddressCreationData,
    AddressCreationRequest,
    AddressCreationWorkflow,
)
from apps.patient_management.addresses.workflows.address_deletion import (
    AddressDeletionData,
    AddressDeletionRequest,
    AddressDeletionWorkflow,
)
from apps.patient_management.addresses.workflows.address_lifecycle import (
    AddressActivationRequest,
    AddressActivationWorkflow,
    AddressDeactivationRequest,
    AddressDeactivationWorkflow,
    AddressLifecycleData,
    AddressPrimaryData,
    AddressPrimaryRequest,
    AddressPrimaryWorkflow,
)
from apps.patient_management.addresses.workflows.address_update import (
    AddressUpdateData,
    AddressUpdateRequest,
    AddressUpdateWorkflow,
)
from apps.patient_management.addresses.workflows.address_verification import (
    AddressVerificationData,
    AddressVerificationRequest,
    AddressVerificationWorkflow,
)

__all__ = (
    "AddressActivationRequest",
    "AddressActivationWorkflow",
    "AddressCreationData",
    "AddressCreationRequest",
    "AddressCreationWorkflow",
    "AddressDeactivationRequest",
    "AddressDeactivationWorkflow",
    "AddressDeletionData",
    "AddressDeletionRequest",
    "AddressDeletionWorkflow",
    "AddressLifecycleData",
    "AddressPrimaryData",
    "AddressPrimaryRequest",
    "AddressPrimaryWorkflow",
    "AddressUpdateData",
    "AddressUpdateRequest",
    "AddressUpdateWorkflow",
    "AddressVerificationData",
    "AddressVerificationRequest",
    "AddressVerificationWorkflow",
)
