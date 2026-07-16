"""
Base vital serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.vitals.models import Vital


class VitalBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for vitals.
    """

    class Meta:
        model = Vital

        fields = (
            "id",
            "organization",
            "patient",
            "provider",
            "encounter",
            "recorded_at",
            "height_cm",
            "weight_kg",
            "bmi",
            "temperature",
            "temperature_unit",
            "pulse",
            "respiratory_rate",
            "systolic_bp",
            "diastolic_bp",
            "oxygen_saturation",
            "pain_score",
            "status",
            "notes",
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
    "VitalBaseSerializer",
]
