"""
Patient Address domain events.
"""

from apps.patient_management.addresses.events.address_created import (
    AddressCreatedEvent,
)
from apps.patient_management.addresses.events.address_deleted import (
    AddressDeletedEvent,
)
from apps.patient_management.addresses.events.address_primary_changed import (
    AddressPrimaryChangedEvent,
)
from apps.patient_management.addresses.events.address_status_changed import (
    AddressStatusChangedEvent,
)
from apps.patient_management.addresses.events.address_updated import (
    AddressUpdatedEvent,
)

__all__ = (
    "AddressCreatedEvent",
    "AddressDeletedEvent",
    "AddressPrimaryChangedEvent",
    "AddressStatusChangedEvent",
    "AddressUpdatedEvent",
)
