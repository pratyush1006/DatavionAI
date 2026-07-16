"""
Base serializers for the Laboratories application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.laboratories.models import (
    LaboratoryTest,
)


class LaboratoryTestSerializer(
    serializers.ModelSerializer,
):
    """
    Base serializer for laboratory tests.
    """

    uuid = serializers.UUIDField(
        source="id",
        read_only=True,
    )

    class Meta:
        """
        Serializer metadata.
        """

        model = LaboratoryTest

        fields = (
            "id",
            "uuid",
            "laboratory_order",
            "code",
            "name",
            "category",
            "specimen_type",
            "priority",
            "status",
            "notes",
            "display_order",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "uuid",
            "status",
            "created_at",
            "updated_at",
        )


__all__ = [
    "LaboratoryTestSerializer",
]
