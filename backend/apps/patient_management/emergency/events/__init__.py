"""Patient emergency domain events."""

from apps.patient_management.emergency.events.created import (
    EmergencyContactCreated,
)
from apps.patient_management.emergency.events.deleted import (
    EmergencyContactDeleted,
)
from apps.patient_management.emergency.events.status_changed import (
    EmergencyContactStatusChanged,
)
from apps.patient_management.emergency.events.updated import (
    EmergencyContactUpdated,
)

__all__ = (
    "EmergencyContactCreated",
    "EmergencyContactDeleted",
    "EmergencyContactStatusChanged",
    "EmergencyContactUpdated",
)
