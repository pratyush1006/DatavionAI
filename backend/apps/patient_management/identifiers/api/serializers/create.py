"""
Serializer for creating patient identifiers.

The serializer validates API input only. Business authorization and
persistence are handled by the workflow and domain service layers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.identifiers.models import PatientIdentifier


class PatientIdentifierCreateSerializer(serializers.ModelSerializer):
    """
    Validate input required to create a patient identifier.
    """

    class Meta:
        model = PatientIdentifier
        fields = (
            "organization",
            "patient",
            "identifier_type",
            "identifier_value",
            "display_value",
            "priority",
            "source",
            "issuing_authority",
            "issuing_country",
            "issued_at",
            "expires_at",
            "system_uri",
            "notes",
            "is_primary",
        )

    def validate_identifier_value(
        self,
        value: str,
    ) -> str:
        """
        Normalize identifier values before passing them to the service.
        """
        return value.strip()

    def validate_display_value(
        self,
        value: str,
    ) -> str:
        """
        Normalize optional display values.
        """
        return value.strip()
