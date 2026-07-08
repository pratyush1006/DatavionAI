"""
Create serializers for the Laboratories application.
"""

from __future__ import annotations

from apps.laboratories.api.serializers.laboratory_test.base import (
    LaboratoryTestSerializer,
)
from apps.laboratories.services import (
    create_laboratory_test,
)


class LaboratoryTestCreateSerializer(
    LaboratoryTestSerializer,
):
    """
    Serializer for creating laboratory tests.
    """

    class Meta(
        LaboratoryTestSerializer.Meta,
    ):
        """
        Serializer metadata.
        """

        read_only_fields = (
            "id",
            "uuid",
            "status",
            "created_at",
            "updated_at",
        )

    def create(
        self,
        validated_data: dict,
    ):
        """
        Create a laboratory test.
        """

        return create_laboratory_test(
            validated_data=validated_data,
        )


__all__ = [
    "LaboratoryTestCreateSerializer",
]
