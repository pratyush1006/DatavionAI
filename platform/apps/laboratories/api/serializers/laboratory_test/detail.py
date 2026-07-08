"""
Detail serializers for the Laboratories application.
"""

from __future__ import annotations

from apps.laboratories.api.serializers.laboratory_test.base import (
    LaboratoryTestSerializer,
)


class LaboratoryTestDetailSerializer(
    LaboratoryTestSerializer,
):
    """
    Serializer for retrieving laboratory test details.
    """

    class Meta(
        LaboratoryTestSerializer.Meta,
    ):
        """
        Serializer metadata.
        """


__all__ = [
    "LaboratoryTestDetailSerializer",
]
