"""
Base diagnosis serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.diagnoses.models import Diagnosis


class DiagnosisBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for diagnoses.
    """

    class Meta:
        model = Diagnosis

        fields = (
            "id",
            "organization",
            "encounter",
            "diagnosis_code",
            "diagnosis_description",
            "diagnosis_type",
            "status",
            "is_primary",
            "present_on_admission",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


__all__ = [
    "DiagnosisBaseSerializer",
]
