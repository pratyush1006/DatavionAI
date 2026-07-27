"""
Serializer for retrieving patient identifier details.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.identifiers.models import (
    PatientIdentifier,
)


class PatientIdentifierDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a patient identifier.
    """

    class Meta:
        model = PatientIdentifier
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
        )
