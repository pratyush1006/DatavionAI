"""
List serializer for Patient Relationships.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class PatientRelationshipListSerializer(
    serializers.ModelSerializer,
):
    """
    Compact representation for relationship collections.
    """

    patient_uuid = serializers.UUIDField(
        source="patient.id",
        read_only=True,
    )

    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )

    related_patient_uuid = serializers.UUIDField(
        source="related_patient.id",
        read_only=True,
        allow_null=True,
    )

    related_patient_name = serializers.CharField(
        source="related_patient.full_name",
        read_only=True,
        allow_null=True,
    )

    organization_uuid = serializers.UUIDField(
        source="organization.id",
        read_only=True,
    )

    class Meta:
        model = PatientRelationship

        fields = (
            "id",
            "patient_uuid",
            "patient_name",
            "related_patient_uuid",
            "related_patient_name",
            "relationship_type",
            "relationship_name",
            "is_primary",
            "status",
            "verification_status",
            "effective_from",
            "effective_to",
            "organization_uuid",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


__all__ = ("PatientRelationshipListSerializer",)
