"""
List serializer for laboratory results.
"""

from __future__ import annotations

from apps.clinical.laboratories.api.serializers.laboratory_result.base import (
    LaboratoryResultSerializer,
)


class LaboratoryResultListSerializer(
    LaboratoryResultSerializer,
):
    """
    Serializer for listing laboratory results.
    """

    class Meta(
        LaboratoryResultSerializer.Meta,
    ):
        """
        Serializer metadata.
        """

        fields = (
            "id",
            "uuid",
            "laboratory_test",
            "result_value_numeric",
            "result_value_text",
            "unit",
            "abnormal_flag",
            "status",
            "resulted_at",
            "verified_by",
        )


__all__ = [
    "LaboratoryResultListSerializer",
]
