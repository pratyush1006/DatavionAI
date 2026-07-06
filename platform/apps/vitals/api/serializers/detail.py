"""
Vital detail serializer.
"""

from __future__ import annotations

from apps.vitals.api.serializers.base import (
    VitalBaseSerializer,
)


class VitalDetailSerializer(
    VitalBaseSerializer,
):
    """
    Serializer for retrieving vital details.
    """


__all__ = [
    "VitalDetailSerializer",
]
