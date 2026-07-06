"""
Appointment list serializer.
"""

from __future__ import annotations

from apps.appointments.api.serializers.base import (
    AppointmentBaseSerializer,
)


class AppointmentListSerializer(
    AppointmentBaseSerializer,
):
    """
    Serializer used for listing appointments.
    """


__all__ = [
    "AppointmentListSerializer",
]
