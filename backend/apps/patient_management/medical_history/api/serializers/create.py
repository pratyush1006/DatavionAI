"""Patient medical history creation serializer.

Validation and payload preparation only.

Medical history creation is performed by MedicalHistoryCreationWorkflow.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.medical_history.models import (
    PatientMedicalHistory,
)


class MedicalHistoryCreateSerializer(serializers.ModelSerializer):
    """
    Validate Patient medical history creation input.

    The organization and patient are explicitly supplied so the workflow
    can enforce tenant and organization boundaries.
    """

    organization_id = serializers.UUIDField(
        write_only=True,
    )
    patient_id = serializers.UUIDField(
        write_only=True,
    )

    class Meta:
        """
        Configure the medical history creation serializer.
        """

        model = PatientMedicalHistory
        fields = (
            "organization_id",
            "patient_id",
            "history_type",
            "title",
            "description",
            "clinical_status",
            "onset_date",
            "resolved_date",
            "relationship",
            "is_smoker",
            "alcohol_use",
            "recorded_by",
        )


__all__ = ("MedicalHistoryCreateSerializer",)
