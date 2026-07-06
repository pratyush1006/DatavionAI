"""
Vital list serializer.
"""

from __future__ import annotations

from apps.vitals.api.serializers.base import (
    VitalBaseSerializer,
)


class VitalListSerializer(
    VitalBaseSerializer,
):
    """
    Serializer for listing vitals.
    """


__all__ = [
    "VitalListSerializer",
]
