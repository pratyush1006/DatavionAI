"""
Create serializer for the Teams application.
"""

from __future__ import annotations

from .base import TeamBaseSerializer
from .fields import WRITE_FIELDS


class TeamCreateSerializer(TeamBaseSerializer):
    """
    Serializer used for creating teams.
    """

    class Meta(TeamBaseSerializer.Meta):
        fields = WRITE_FIELDS


__all__ = [
    "TeamCreateSerializer",
]
