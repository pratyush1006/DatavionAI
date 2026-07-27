"""
Detail serializer for Patient Relationships.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class RelationshipDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a patient relationship.
    """

    class Meta:
        model = PatientRelationship
        fields = "__all__"
