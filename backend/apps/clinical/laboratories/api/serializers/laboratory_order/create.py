"""
Create serializers for the Laboratories application.
"""

from __future__ import annotations

from apps.clinical.laboratories.api.serializers.laboratory_order.base import (
    LaboratoryOrderSerializer,
)
from apps.clinical.laboratories.services import (
    create_laboratory_order,
)


class LaboratoryOrderCreateSerializer(
    LaboratoryOrderSerializer,
):
    """
    Serializer for creating laboratory orders.
    """

    class Meta(
        LaboratoryOrderSerializer.Meta,
    ):
        """
        Serializer metadata.
        """

        read_only_fields = (
            "id",
            "status",
            "created_at",
            "updated_at",
        )

    def create(
        self,
        validated_data: dict,
    ):
        """
        Create a laboratory order.
        """

        return create_laboratory_order(
            validated_data=validated_data,
        )


__all__ = [
    "LaboratoryOrderCreateSerializer",
]
