"""
Base serializers for the Laboratories application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.laboratories.models import (
    LaboratoryOrder,
)


class LaboratoryOrderSerializer(
    serializers.ModelSerializer,
):
    """
    Base serializer for laboratory orders.
    """

    uuid = serializers.UUIDField(
        source="id",
        read_only=True,
    )

    class Meta:
        """
        Serializer metadata.
        """

        model = LaboratoryOrder

        fields = (
            "id",
            "uuid",
            "organization",
            "patient",
            "provider",
            "encounter",
            "order_number",
            "priority",
            "status",
            "ordered_at",
            "clinical_notes",
            "instructions",
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
    "LaboratoryOrderSerializer",
]
