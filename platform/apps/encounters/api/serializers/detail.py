"""
Encounter detail serializer.
"""

from __future__ import annotations

from apps.encounters.api.serializers.base import (
    EncounterBaseSerializer,
)
from apps.encounters.api.serializers.fields import (
    AppointmentFieldSerializer,
    PatientFieldSerializer,
    ProviderFieldSerializer,
)


class EncounterDetailSerializer(
    EncounterBaseSerializer,
):
    """
    Serializer for encounter detail endpoint.
    """

    patient = PatientFieldSerializer(
        read_only=True,
    )

    provider = ProviderFieldSerializer(
        read_only=True,
    )

    appointment = AppointmentFieldSerializer(
        read_only=True,
    )


__all__ = [
    "EncounterDetailSerializer",
]
