"""
Appointment permission exports.
"""

from .appointment import (
    CanCreateAppointment,
    CanDeleteAppointment,
    CanUpdateAppointment,
    CanViewAppointment,
)

__all__ = [
    "CanCreateAppointment",
    "CanDeleteAppointment",
    "CanUpdateAppointment",
    "CanViewAppointment",
]
