"""
Vital update serializer.
"""

from __future__ import annotations

from apps.vitals.api.serializers.base import (
    VitalBaseSerializer,
)


class VitalUpdateSerializer(
    VitalBaseSerializer,
):
    """
    Serializer for updating vitals.
    """


__all__ = [
    "VitalUpdateSerializer",
]
