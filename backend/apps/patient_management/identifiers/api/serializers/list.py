"""
Serializer for listing patient identifiers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.identifiers.models import (
    PatientIdentifier,
)


class PatientIdentifierListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing patient identifiers.
    """

    class Meta:
        model = PatientIdentifier
        fields = (
            "id",
            "identifier_type",
            "identifier_value",
            "display_value",
            "status",
            "verification_status",
            "is_primary",
            "source",
            "issued_at",
            "expires_at",
        )
        read_only_fields = fields
