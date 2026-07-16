"""
Update serializers for the Laboratories application.
"""

from __future__ import annotations

from apps.clinical.laboratories.api.serializers.laboratory_test.base import (
    LaboratoryTestSerializer,
)
from apps.clinical.laboratories.services import (
    update_laboratory_test,
)


class LaboratoryTestUpdateSerializer(
    LaboratoryTestSerializer,
):
    """
    Serializer for updating laboratory tests.
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
            "laboratory_order",
            "code",
            "category",
            "specimen_type",
            "status",
            "created_at",
            "updated_at",
        )

    def update(
        self,
        instance,
        validated_data: dict,
    ):
        """
        Update a laboratory test.
        """

        return update_laboratory_test(
            instance=instance,
            validated_data=validated_data,
        )


__all__ = [
    "LaboratoryTestUpdateSerializer",
]
