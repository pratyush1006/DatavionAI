"""Patient guarantor API serializers."""

from __future__ import annotations

from apps.billing.patient_billing.models import PatientGuarantor
from rest_framework import serializers


class PatientGuarantorSerializer(serializers.ModelSerializer):
    """Serialize patient guarantors."""

    class Meta:
        """Serializer metadata."""

        model = PatientGuarantor
        fields = (
            "id",
            "organization",
            "patient",
            "name",
            "relationship",
            "phone",
            "email",
            "address",
            "is_primary",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "organization",
            "patient",
            "is_active",
            "created_at",
            "updated_at",
        )


class PatientGuarantorCreateSerializer(serializers.ModelSerializer):
    """Validate guarantor creation."""

    class Meta:
        """Serializer metadata."""

        model = PatientGuarantor
        fields = (
            "patient",
            "name",
            "relationship",
            "phone",
            "email",
            "address",
            "is_primary",
        )

    def validate_name(self, value: str) -> str:
        """Require a non-empty guarantor name."""

        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Guarantor name is required.",
            )
        return value


class PatientGuarantorUpdateSerializer(serializers.ModelSerializer):
    """Validate guarantor updates."""

    class Meta:
        """Serializer metadata."""

        model = PatientGuarantor
        fields = (
            "name",
            "relationship",
            "phone",
            "email",
            "address",
            "is_primary",
        )


__all__ = (
    "PatientGuarantorCreateSerializer",
    "PatientGuarantorSerializer",
    "PatientGuarantorUpdateSerializer",
)
