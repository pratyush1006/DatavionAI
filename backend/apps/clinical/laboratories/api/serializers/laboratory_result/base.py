"""
Base serializers for the Laboratories application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.laboratories.models import (
    LaboratoryResult,
)


class LaboratoryResultSerializer(
    serializers.ModelSerializer,
):
    """
    Base serializer for laboratory results.
    """

    uuid = serializers.UUIDField(
        source="id",
        read_only=True,
    )

    class Meta:
        """
        Serializer metadata.
        """

        model = LaboratoryResult

        fields = (
            "id",
            "uuid",
            "laboratory_test",
            "result_value_numeric",
            "result_value_text",
            "unit",
            "reference_range",
            "abnormal_flag",
            "status",
            "resulted_at",
            "verified_by",
            "verified_at",
            "notes",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "uuid",
            "status",
            "verified_by",
            "verified_at",
            "created_at",
            "updated_at",
        )


__all__ = [
    "LaboratoryResultSerializer",
]
