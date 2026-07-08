"""
Create serializers for the Laboratories application.
"""

from __future__ import annotations

from apps.laboratories.api.serializers.laboratory_result.base import (
    LaboratoryResultSerializer,
)
from apps.laboratories.services import (
    create_laboratory_result,
)


class LaboratoryResultCreateSerializer(
    LaboratoryResultSerializer,
):
    """
    Serializer for creating laboratory results.
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
            "status",
            "verified_by",
            "verified_at",
            "created_at",
            "updated_at",
        )

    def create(
        self,
        validated_data: dict,
    ):
        """
        Create a laboratory result.
        """

        return create_laboratory_result(
            validated_data=validated_data,
        )


__all__ = [
    "LaboratoryResultCreateSerializer",
]
