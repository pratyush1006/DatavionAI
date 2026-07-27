"""
Update serializer for Patient Relationships.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class RelationshipUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a patient relationship.
    """

    class Meta:
        model = PatientRelationship
        fields = (
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
