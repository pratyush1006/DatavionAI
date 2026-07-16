"""
Encounter update serializer.
"""

from __future__ import annotations

from apps.clinical.encounters.api.serializers.base import (
    EncounterBaseSerializer,
)


class EncounterUpdateSerializer(
    EncounterBaseSerializer,
):
    """
    Serializer used when updating encounters.
    """


__all__ = [
    "EncounterUpdateSerializer",
]
