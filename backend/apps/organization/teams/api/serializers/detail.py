"""
Detail serializer for Teams.
"""

from __future__ import annotations

from rest_framework import serializers

from .base import TeamBaseSerializer


class TeamDetailSerializer(
    TeamBaseSerializer,
):
    """
    Detailed Team representation.
    """

    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.UUIDField(
        source="organization.id",
        read_only=True,
    )

    class Meta(
        TeamBaseSerializer.Meta,
    ):
        fields = (
            "id",
            "organization",
            "organization_id",
            "name",
            "code",
            "description",
            "team_type",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


__all__ = ("TeamDetailSerializer",)
