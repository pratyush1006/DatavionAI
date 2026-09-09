"""
Emergency Contacts domain events.
"""

from .emergency_contact_created import (
    EmergencyContactCreatedEvent,
)
from .emergency_contact_deleted import (
    EmergencyContactDeletedEvent,
)
from .emergency_contact_primary_changed import (
    EmergencyContactPrimaryChangedEvent,
)
from .emergency_contact_status_changed import (
    EmergencyContactStatusChangedEvent,
)
from .emergency_contact_updated import (
    EmergencyContactUpdatedEvent,
)
from .emergency_contact_verified import (
    EmergencyContactVerifiedEvent,
)

__all__ = (
    "EmergencyContactCreatedEvent",
    "EmergencyContactDeletedEvent",
    "EmergencyContactPrimaryChangedEvent",
    "EmergencyContactStatusChangedEvent",
    "EmergencyContactUpdatedEvent",
    "EmergencyContactVerifiedEvent",
)
