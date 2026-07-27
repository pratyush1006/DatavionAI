"""
Update serializer for the Patients application.
"""

from __future__ import annotations

from apps.clinical.patients.models import Patient
from apps.clinical.patients.services import PatientService

from .base import PatientBaseSerializer
from .fields import (
    READ_ONLY_FIELDS,
    UPDATE_FIELDS,
)


class PatientUpdateSerializer(PatientBaseSerializer):
    """
    Serializer used for updating patients.
    """

    class Meta(PatientBaseSerializer.Meta):
        fields = UPDATE_FIELDS
        read_only_fields = READ_ONLY_FIELDS

    def update(
        self,
        instance: Patient,
        validated_data: dict[str, object],
    ) -> Patient:
        """
        Update a patient.
        """

        return PatientService.update(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "PatientUpdateSerializer",
]
