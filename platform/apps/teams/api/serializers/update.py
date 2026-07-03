"""
Update serializer for the Teams application.
"""

from __future__ import annotations

from .base import TeamBaseSerializer
from .fields import UPDATE_FIELDS


class TeamUpdateSerializer(TeamBaseSerializer):
    """
    Serializer used for updating teams.
    """

    class Meta(TeamBaseSerializer.Meta):
        fields = UPDATE_FIELDS


__all__ = [
    "TeamUpdateSerializer",
]
