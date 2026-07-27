"""
List serializer for Patient Relationships.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class RelationshipListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing patient relationships.
    """

    class Meta:
        model = PatientRelationship
        fields = (
            "id",
            "patient",
            "related_patient",
            "relationship_type",
            "relationship_name",
            "status",
            "verification_status",
            "is_primary",
        )
