"""
Appointment permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanViewAppointment(BasePermission):
    """
    Permission required to view appointments.
    """

    permission_code = "appointment.view"


class CanCreateAppointment(BasePermission):
    """
    Permission required to create appointments.
    """

    permission_code = "appointment.create"


class CanUpdateAppointment(BasePermission):
    """
    Permission required to update appointments.
    """

    permission_code = "appointment.update"


class CanDeleteAppointment(BasePermission):
    """
    Permission required to delete appointments.
    """

    permission_code = "appointment.delete"


__all__ = [
    "CanCreateAppointment",
    "CanDeleteAppointment",
    "CanUpdateAppointment",
    "CanViewAppointment",
]
