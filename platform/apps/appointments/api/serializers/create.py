"""
Appointment create serializer.
"""

from __future__ import annotations

from apps.appointments.api.serializers.base import (
    AppointmentBaseSerializer,
)


class AppointmentCreateSerializer(
    AppointmentBaseSerializer,
):
    """
    Serializer for creating appointments.
    """

    pass


__all__ = [
    "AppointmentCreateSerializer",
]
