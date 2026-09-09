"""
Patient API base serializers.

Serializers are responsible only for:

- HTTP payload validation
- field normalization
- representation

Business operations belong to workflows/services.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patients.models import Patient


class PatientBaseSerializer(serializers.ModelSerializer):
    """
    Common Patient serializer.

    The serializer deliberately does not perform model mutations.
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

        read_only_fields = (
            "id",
            "display_name",
            "age",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )

    def validate_first_name(self, value: str) -> str:
        return value.strip()

    def validate_middle_name(self, value: str) -> str:
        return value.strip()

    def validate_last_name(self, value: str) -> str:
        return value.strip()

    def validate_preferred_name(self, value: str) -> str:
        return value.strip()

    def validate_mrn(self, value: str) -> str:
        return value.strip().upper()

    def validate_email(self, value: str) -> str:
        return value.strip().lower()

    def validate_phone(self, value: str) -> str:
        return value.strip()

    def validate_city(self, value: str) -> str:
        return value.strip()

    def validate_state(self, value: str) -> str:
        return value.strip()

    def validate_country(self, value: str) -> str:
        return value.strip()

    def validate_postal_code(self, value: str) -> str:
        return value.strip()

    def validate_address(self, value: str) -> str:
        return value.strip()


__all__ = ("PatientBaseSerializer",)
