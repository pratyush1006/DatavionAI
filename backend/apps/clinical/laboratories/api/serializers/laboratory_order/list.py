"""
List serializers for the Laboratories application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.clinical.laboratories.models import (
    LaboratoryOrder,
)


class LaboratoryOrderListSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for listing laboratory orders.
    """

    uuid = serializers.UUIDField(
        source="id",
        read_only=True,
    )

    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True,
    )

    provider_name = serializers.CharField(
        source="provider.full_name",
        read_only=True,
    )

    class Meta:
        model = LaboratoryOrder

        fields = (
            "id",
            "uuid",
            "order_number",
            "patient_name",
            "provider_name",
            "priority",
            "status",
            "ordered_at",
        )

        read_only_fields = fields


__all__ = [
    "LaboratoryOrderListSerializer",
]
