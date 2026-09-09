"""
Patient Contact domain events.

Public event exports for the Contacts bounded context.
"""

from apps.patient_management.contacts.events.contact_created import (
    ContactCreatedEvent,
)
from apps.patient_management.contacts.events.contact_deleted import (
    ContactDeletedEvent,
)
from apps.patient_management.contacts.events.contact_primary_changed import (
    ContactPrimaryChangedEvent,
)
from apps.patient_management.contacts.events.contact_status_changed import (
    ContactStatusChangedEvent,
)
from apps.patient_management.contacts.events.contact_updated import (
    ContactUpdatedEvent,
)
from apps.patient_management.contacts.events.contact_verified import (
    ContactVerifiedEvent,
)

__all__ = (
    "ContactCreatedEvent",
    "ContactDeletedEvent",
    "ContactPrimaryChangedEvent",
    "ContactStatusChangedEvent",
    "ContactUpdatedEvent",
    "ContactVerifiedEvent",
)
