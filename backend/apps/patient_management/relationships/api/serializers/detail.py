"""
Detail serializer for Patient Relationships.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class PatientRelationshipDetailSerializer(
    serializers.ModelSerializer,
):
    """
    Full read representation of a Patient Relationship.
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

    is_external = serializers.BooleanField(
        read_only=True,
    )

    is_verified = serializers.BooleanField(
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
            "notes",
            "organization_uuid",
            "is_external",
            "is_verified",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


__all__ = ("PatientRelationshipDetailSerializer",)
