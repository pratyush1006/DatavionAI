"""
Serializer for updating patient identifiers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.identifiers.models import (
    PatientIdentifier,
)


class PatientIdentifierUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a patient identifier.
    """

    class Meta:
        model = PatientIdentifier
        exclude = (
            "id",
            "organization",
            "patient",
            "created_at",
            "updated_at",
            "deleted_at",
            "verified_at",
            "verified_by",
        )

        read_only_fields = ("verification_status",)
