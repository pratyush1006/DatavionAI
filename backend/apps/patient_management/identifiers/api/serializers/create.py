"""
Serializer for creating patient identifiers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.identifiers.models import (
    PatientIdentifier,
)


class PatientIdentifierCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a patient identifier.
    """

    class Meta:
        model = PatientIdentifier
        exclude = (
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "verified_at",
            "verified_by",
        )

        read_only_fields = ("verification_status",)
