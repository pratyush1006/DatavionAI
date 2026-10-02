"""
Serializer for updating patient identifiers.

Lifecycle and verification changes must go through their dedicated
workflows rather than generic update.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.identifiers.models import PatientIdentifier


class PatientIdentifierUpdateSerializer(serializers.ModelSerializer):
    """
    Validate mutable patient identifier fields.
    """

    class Meta:
        model = PatientIdentifier
        fields = (
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
