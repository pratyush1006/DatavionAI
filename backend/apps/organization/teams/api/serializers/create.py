"""
Create serializer for Teams application.
"""

from __future__ import annotations

from rest_framework import serializers

from .base import TeamBaseSerializer
from .fields import WRITE_FIELDS


class TeamCreateSerializer(
    TeamBaseSerializer,
):
    """
    Serializer used for creating teams.
    """

    class Meta(
        TeamBaseSerializer.Meta,
    ):
        fields = WRITE_FIELDS

    def validate(
        self,
        attrs,
    ):
        """
        Validate team creation data.
        """

        organization = attrs.get(
            "organization",
        )

        if organization is None:
            raise serializers.ValidationError(
                {"organization": ("Organization is required.")}
            )

        return attrs


__all__ = ("TeamCreateSerializer",)
