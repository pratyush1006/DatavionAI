"""
List serializer for Teams.
"""

from __future__ import annotations

from rest_framework import serializers

from .base import TeamBaseSerializer
from .fields import LIST_FIELDS


class TeamListSerializer(
    TeamBaseSerializer,
):
    """
    Serializer used for team listing.
    """

    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta(
        TeamBaseSerializer.Meta,
    ):
        fields = (*LIST_FIELDS,)

        read_only_fields = fields


__all__ = ("TeamListSerializer",)
