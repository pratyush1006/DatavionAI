"""
Patient detail serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patients.models import Patient


class PatientDetailSerializer(serializers.ModelSerializer):
    """
    Complete read representation of a Patient.
    """

    class Meta:
        model = Patient

        fields = (
            "id",
            "organization",
            "mrn",
            "first_name",
            "middle_name",
            "last_name",
            "preferred_name",
            "display_name",
            "date_of_birth",
            "age",
            "gender",
            "marital_status",
            "blood_group",
            "phone",
            "email",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


__all__ = ("PatientDetailSerializer",)
