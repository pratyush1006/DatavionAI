"""
Update serializer for Patient Relationships.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.relationships.models import (
    PatientRelationship,
)


class PatientRelationshipUpdateSerializer(
    serializers.ModelSerializer,
):
    """
    Validate mutable Patient Relationship fields.

    Lifecycle and verification transitions are deliberately excluded from
    ordinary update requests.
    """

    class Meta:
        model = PatientRelationship
        fields = (
            "related_patient",
            "relationship_type",
            "relationship_name",
            "effective_from",
            "effective_to",
            "notes",
        )

        read_only_fields = (
            "patient",
            "organization",
            "status",
            "verification_status",
            "is_primary",
        )

    def validate(self, attrs: dict) -> dict:
        """
        Validate update-specific input without performing persistence.
        """
        instance = self.instance

        if instance is not None:
            related_patient = attrs.get(
                "related_patient",
                instance.related_patient,
            )

            if (
                related_patient is not None
                and related_patient.pk == instance.patient_id
            ):
                raise serializers.ValidationError(
                    {
                        "related_patient": (
                            "A patient cannot have a relationship with themselves."
                        ),
                    },
                )

            relationship_name = attrs.get(
                "relationship_name",
                instance.relationship_name,
            )

            if (
                related_patient is None
                and not str(
                    relationship_name or "",
                ).strip()
            ):
                raise serializers.ValidationError(
                    {
                        "relationship_name": (
                            "A relationship name is required when "
                            "the related patient is external."
                        ),
                    },
                )

        return attrs


__all__ = ("PatientRelationshipUpdateSerializer",)
