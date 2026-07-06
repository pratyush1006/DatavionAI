"""
Vital create serializer.
"""

from __future__ import annotations

from apps.vitals.api.serializers.base import (
    VitalBaseSerializer,
)


class VitalCreateSerializer(
    VitalBaseSerializer,
):
    """
    Serializer for creating vitals.
    """


__all__ = [
    "VitalCreateSerializer",
]
