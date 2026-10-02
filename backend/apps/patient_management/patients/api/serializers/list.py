"""
Patient list serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patients.models import Patient


class PatientListSerializer(serializers.ModelSerializer):
    """
    Lightweight Patient representation for collection responses.
    """

    class Meta:
        model = Patient

        fields = (
            "id",
            "mrn",
            "display_name",
            "gender",
            "date_of_birth",
            "phone",
            "email",
            "status",
            "is_active",
        )

        read_only_fields = fields


__all__ = ("PatientListSerializer",)
