"""Patient medical history update serializer.

Validation and payload preparation only.

Medical history updates are performed by MedicalHistoryUpdateWorkflow.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.medical_history.models import (
    PatientMedicalHistory,
)


class MedicalHistoryUpdateSerializer(serializers.ModelSerializer):
    """
    Validate Patient medical history update input.

    Patient identity and organization boundaries remain controlled by the
    workflow and are not accepted as mutable serializer fields.
    """

    class Meta:
        """
        Configure the medical history update serializer.
        """

        model = PatientMedicalHistory
        fields = (
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


__all__ = ("MedicalHistoryUpdateSerializer",)
