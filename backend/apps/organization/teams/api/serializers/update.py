"""
Update serializer for Teams.
"""

from __future__ import annotations

from .base import TeamBaseSerializer
from .fields import UPDATE_FIELDS


class TeamUpdateSerializer(
    TeamBaseSerializer,
):
    """
    Serializer used for updating teams.
    """

    class Meta(
        TeamBaseSerializer.Meta,
    ):
        fields = UPDATE_FIELDS

        read_only_fields = ("organization",)


__all__ = ("TeamUpdateSerializer",)
