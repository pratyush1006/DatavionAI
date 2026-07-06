"""
Base allergy serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.allergies.models import Allergy


class AllergyBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for allergies.
    """

    class Meta:
        model = Allergy

        fields = (
            "id",
            "organization",
            "patient",
            "provider",
            "encounter",
            "allergen",
            "category",
            "severity",
            "status",
            "reaction",
            "onset_date",
            "resolved_date",
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
    "AllergyBaseSerializer",
]
