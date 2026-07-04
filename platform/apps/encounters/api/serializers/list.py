"""
Encounter list serializer.
"""

from __future__ import annotations

from apps.encounters.api.serializers.base import (
    EncounterBaseSerializer,
)


class EncounterListSerializer(
    EncounterBaseSerializer,
):
    """
    Serializer for encounter list endpoint.
    """

    pass


__all__ = [
    "EncounterListSerializer",
]
