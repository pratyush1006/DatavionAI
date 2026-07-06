"""
Encounter create serializer.
"""

from __future__ import annotations

from apps.encounters.api.serializers.base import (
    EncounterBaseSerializer,
)


class EncounterCreateSerializer(
    EncounterBaseSerializer,
):
    """
    Serializer used when creating encounters.
    """


__all__ = [
    "EncounterCreateSerializer",
]
