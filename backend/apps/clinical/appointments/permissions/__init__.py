"""Clinical Appointment permission package."""

from apps.clinical.appointments.permissions.api import AppointmentAPIPermission
from apps.clinical.appointments.permissions.appointment import (
    PERMISSION_CODES,
    AppointmentPermission,
)

__all__ = (
    "AppointmentPermission",
    "AppointmentAPIPermission",
    "PERMISSION_CODES",
)
