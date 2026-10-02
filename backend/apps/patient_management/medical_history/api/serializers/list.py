"""Patient medical history list serializer.

Provides the compact representation used by medical history collection
endpoints.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.medical_history.models import (
    PatientMedicalHistory,
)


class MedicalHistoryListSerializer(serializers.ModelSerializer):
    """
    Serialize a patient medical history record for list views.

    The list representation intentionally contains only fields required
    for collection-level presentation.
    """

    class Meta:
        """
        Configure the medical history list serializer.
        """

        model = PatientMedicalHistory
        fields = (
            "id",
            "patient_id",
            "history_type",
            "title",
            "clinical_status",
            "onset_date",
            "resolved_date",
            "is_active",
            "is_verified",
            "created_at",
            "updated_at",
        )


__all__ = ("MedicalHistoryListSerializer",)
