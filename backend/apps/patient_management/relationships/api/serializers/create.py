"""
Create serializer for Patient Relationships.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class PatientRelationshipCreateSerializer(
    serializers.ModelSerializer,
):
    """
    Validate client-supplied Patient Relationship creation data.

    Organization is resolved from authenticated request context by the API
    workflow layer and is never accepted as client-controlled input.
    """

    class Meta:
        model = PatientRelationship
        fields = (
            "patient",
            "related_patient",
            "relationship_type",
            "relationship_name",
            "effective_from",
            "effective_to",
            "notes",
        )

    def validate(self, attrs: dict) -> dict:
        """
        Perform serializer-level input validation only.

        Domain invariants remain owned by the model/service layer.
        """
        patient = attrs.get("patient")
        related_patient = attrs.get("related_patient")

        if (
            patient is not None
            and related_patient is not None
            and patient.pk == related_patient.pk
        ):
            raise serializers.ValidationError(
                {
                    "related_patient": (
                        "A patient cannot have a relationship with themselves."
                    ),
                },
            )

        if (
            related_patient is None
            and not str(
                attrs.get(
                    "relationship_name",
                    "",
                ),
            ).strip()
        ):
            raise serializers.ValidationError(
                {
                    "relationship_name": (
                        "A relationship name is required when the "
                        "related patient is external."
                    ),
                },
            )

        return attrs


__all__ = ("PatientRelationshipCreateSerializer",)
