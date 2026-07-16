"""
Update serializers for the Laboratories application.
"""

from __future__ import annotations

from typing import Any

from apps.clinical.laboratories.api.serializers.laboratory_result.base import (
    LaboratoryResultSerializer,
)
from apps.clinical.laboratories.services import (
    update_laboratory_result,
)


class LaboratoryResultUpdateSerializer(
    LaboratoryResultSerializer,
):
    """
    Serializer for updating laboratory results.
    """

    class Meta(
        LaboratoryResultSerializer.Meta,
    ):
        """
        Serializer metadata.
        """

        read_only_fields = (
            "id",
            "uuid",
            "laboratory_test",
            "status",
            "verified_by",
            "verified_at",
            "created_at",
            "updated_at",
        )

    def update(
        self,
        instance,
        validated_data: dict[str, Any],
    ):
        """
        Update a laboratory result.
        """

        return update_laboratory_result(
            laboratory_result_id=instance.pk,
            validated_data=validated_data,
        )


__all__ = [
    "LaboratoryResultUpdateSerializer",
]
