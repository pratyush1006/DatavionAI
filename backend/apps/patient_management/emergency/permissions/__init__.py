"""Patient emergency permission package."""

from apps.patient_management.emergency.permissions.emergency import (
    PERMISSION_CODES,
    EmergencyPermission,
)

__all__ = (
    "EmergencyPermission",
    "PERMISSION_CODES",
)
