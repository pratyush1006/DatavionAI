"""
Update serializers for the Laboratories application.
"""

from __future__ import annotations

from typing import Any

from apps.clinical.laboratories.api.serializers.laboratory_order.base import (
    LaboratoryOrderSerializer,
)
from apps.clinical.laboratories.services import (
    update_laboratory_order,
)


class LaboratoryOrderUpdateSerializer(
    LaboratoryOrderSerializer,
):
    """
    Serializer for updating laboratory orders.
    """

    class Meta(
        LaboratoryOrderSerializer.Meta,
    ):
        """
        Serializer metadata.
        """

        read_only_fields = (
            "id",
            "uuid",
            "organization",
            "patient",
            "provider",
            "encounter",
            "order_number",
            "status",
            "created_at",
            "updated_at",
        )

    def update(
        self,
        instance,
        validated_data: dict[str, Any],
    ):
        """
        Update a laboratory order.
        """

        return update_laboratory_order(
            laboratory_order_id=instance.pk,
            validated_data=validated_data,
        )


__all__ = [
    "LaboratoryOrderUpdateSerializer",
]
