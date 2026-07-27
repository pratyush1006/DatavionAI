"""
Create serializer for the Patients application.
"""

from __future__ import annotations

from apps.clinical.patients.services import PatientService

from .base import PatientBaseSerializer
from .fields import (
    READ_ONLY_FIELDS,
    WRITE_FIELDS,
)


class PatientCreateSerializer(PatientBaseSerializer):
    """
    Serializer used for creating patients.
    """

    class Meta(PatientBaseSerializer.Meta):
        fields = WRITE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def create(
        self,
        validated_data: dict[str, object],
    ):
        """
        Create a patient.
        """

        return PatientService.create(
            validated_data=validated_data,
        )


__all__ = [
    "PatientCreateSerializer",
]
