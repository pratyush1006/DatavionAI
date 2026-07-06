"""
Appointment update serializer.
"""

from __future__ import annotations

from apps.appointments.api.serializers.base import (
    AppointmentBaseSerializer,
)


class AppointmentUpdateSerializer(
    AppointmentBaseSerializer,
):
    """
    Serializer for updating appointments.
    """


__all__ = [
    "AppointmentUpdateSerializer",
]
