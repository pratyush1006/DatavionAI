"""Patient medical history detail serializer.

Provides the read-only representation used by medical history detail
endpoints.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.medical_history.models import (
    PatientMedicalHistory,
)


class MedicalHistoryDetailSerializer(serializers.ModelSerializer):
    """
    Serialize a patient medical history record for detail views.

    Display labels are exposed alongside stored choice values for
    presentation-layer consumers.
    """

    patient_name = serializers.SerializerMethodField()
    history_type_label = serializers.CharField(
        source="get_history_type_display",
        read_only=True,
    )
    clinical_status_label = serializers.CharField(
        source="get_clinical_status_display",
        read_only=True,
    )

    class Meta:
        """
        Configure the medical history detail serializer.
        """

        model = PatientMedicalHistory
        fields = (
            "id",
            "patient_id",
            "patient_name",
            "organization_id",
            "history_type",
            "history_type_label",
            "title",
            "description",
            "clinical_status",
            "clinical_status_label",
            "onset_date",
            "resolved_date",
            "relationship",
            "is_smoker",
            "alcohol_use",
            "recorded_by",
            "is_active",
            "is_deleted",
            "is_verified",
            "verified_at",
            "verified_by",
            "created_at",
            "updated_at",
        )

    def get_patient_name(
        self,
        obj: PatientMedicalHistory,
    ) -> str:
        """
        Return the display name of the related patient.
        """

        return str(obj.patient)


__all__ = ("MedicalHistoryDetailSerializer",)
