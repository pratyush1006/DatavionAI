"""
Appointment detail serializer.
"""

from __future__ import annotations

from apps.appointments.api.serializers.base import (
    AppointmentBaseSerializer,
)


class AppointmentDetailSerializer(
    AppointmentBaseSerializer,
):
    """
    Serializer used for retrieving appointments.
    """

    pass


__all__ = [
    "AppointmentDetailSerializer",
]
