"""
Serializer for retrieving patient identifier details.

The detail representation intentionally masks the raw identifier value.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.identifiers.models import PatientIdentifier


class PatientIdentifierDetailSerializer(serializers.ModelSerializer):
    """
    Safe detailed representation of a patient identifier.
    """

    masked_value = serializers.SerializerMethodField()

    class Meta:
        model = PatientIdentifier
        fields = (
            "id",
            "organization",
            "patient",
            "identifier_type",
            "display_value",
            "masked_value",
            "priority",
            "status",
            "verification_status",
            "source",
            "issuing_authority",
            "issuing_country",
            "issued_at",
            "expires_at",
            "verified_at",
            "verified_by",
            "system_uri",
            "notes",
            "is_primary",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields

    def get_masked_value(
        self,
        instance: PatientIdentifier,
    ) -> str:
        """
        Return a privacy-preserving representation of the identifier.
        """
        value = instance.identifier_value or ""

        if len(value) <= 4:
            return "*" * len(value)

        return f"{'*' * (len(value) - 4)}{value[-4:]}"
