"""
Encounter update serializer.
"""

from __future__ import annotations

from apps.encounters.api.serializers.base import (
    EncounterBaseSerializer,
)


class EncounterUpdateSerializer(
    EncounterBaseSerializer,
):
    """
    Serializer used when updating encounters.
    """

    pass


__all__ = [
    "EncounterUpdateSerializer",
]
