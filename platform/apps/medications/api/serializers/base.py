"""
Base medication serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.medications.models import Medication


class MedicationBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for medications.
    """

    class Meta:
        model = Medication

        fields = (
            "id",
            "organization",
            "medication_code",
            "generic_name",
            "brand_name",
            "strength",
            "strength_unit",
            "dosage_form",
            "route",
            "manufacturer",
            "description",
            "is_controlled",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


__all__ = [
    "MedicationBaseSerializer",
]
