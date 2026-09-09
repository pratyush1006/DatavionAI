"""
Serializer for listing patient identifiers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.identifiers.models import PatientIdentifier


class PatientIdentifierListSerializer(serializers.ModelSerializer):
    """
    Safe list representation of a patient identifier.

    Raw identifier values are never returned by collection endpoints.
    """

    masked_value = serializers.SerializerMethodField()

    class Meta:
        model = PatientIdentifier
        fields = (
            "id",
            "identifier_type",
            "display_value",
            "masked_value",
            "priority",
            "status",
            "verification_status",
            "is_primary",
            "source",
            "issued_at",
            "expires_at",
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
