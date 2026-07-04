"""
Appointment selectors.
"""

from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.appointments.models import Appointment


def get_appointments() -> QuerySet[Appointment]:
    """
    Return the appointments queryset.
    """

    return Appointment.objects.select_related(
        "organization",
        "patient",
        "provider",
        "provider__employee",
        "provider__employee__user",
    )


def get_appointment_by_id(
    *,
    appointment_id,
) -> Appointment:
    """
    Return an appointment by ID.
    """

    return get_object_or_404(
        get_appointments(),
        id=appointment_id,
    )


__all__ = [
    "get_appointment_by_id",
    "get_appointments",
]
