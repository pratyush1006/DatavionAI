"""
List serializers for the Laboratories application.
"""

from __future__ import annotations

from apps.clinical.laboratories.api.serializers.laboratory_test.base import (
    LaboratoryTestSerializer,
)


class LaboratoryTestListSerializer(
    LaboratoryTestSerializer,
):
    """
    Serializer for listing laboratory tests.
    """

    class Meta(
        LaboratoryTestSerializer.Meta,
    ):
        """
        Serializer metadata.
        """


__all__ = [
    "LaboratoryTestListSerializer",
]
