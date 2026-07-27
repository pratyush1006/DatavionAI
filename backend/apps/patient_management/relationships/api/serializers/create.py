"""
Create serializer for Patient Relationships.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class RelationshipCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a patient relationship.
    """

    class Meta:
        model = PatientRelationship
        fields = (
            "id",
            "organization",
            "patient",
            "related_patient",
            "relationship_type",
            "relationship_name",
            "relationship_strength",
            "status",
            "verification_status",
            "source",
            "is_primary",
            "start_date",
            "end_date",
            "notes",
        )
