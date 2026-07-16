"""
Detail serializer for laboratory results.
"""

from __future__ import annotations

from apps.clinical.laboratories.api.serializers.laboratory_result.base import (
    LaboratoryResultSerializer,
)


class LaboratoryResultDetailSerializer(
    LaboratoryResultSerializer,
):
    """
    Serializer for retrieving a laboratory result.
    """

    class Meta(
        LaboratoryResultSerializer.Meta,
    ):
        """
        Serializer metadata.
        """

        fields = LaboratoryResultSerializer.Meta.fields


__all__ = [
    "LaboratoryResultDetailSerializer",
]
