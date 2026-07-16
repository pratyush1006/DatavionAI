"""
Appointment detail serializer.
"""

from __future__ import annotations

from apps.clinical.appointments.api.serializers.base import (
    AppointmentBaseSerializer,
)


class AppointmentDetailSerializer(
    AppointmentBaseSerializer,
):
    """
    Serializer used for retrieving appointments.
    """


__all__ = [
    "AppointmentDetailSerializer",
]
