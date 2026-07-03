"""
Detail serializer for the Teams application.
"""

from __future__ import annotations

from rest_framework import serializers

from .base import TeamBaseSerializer


class TeamDetailSerializer(TeamBaseSerializer):
    """
    Serializer used for retrieving a team.
    """

    department = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    department_id = serializers.IntegerField(
        source="department.id",
        read_only=True,
    )

    organization = serializers.CharField(
        source="department.organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="department.organization.id",
        read_only=True,
    )

    class Meta(TeamBaseSerializer.Meta):
        fields = (
            "id",
            "organization",
            "organization_id",
            "department",
            "department_id",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


__all__ = [
    "TeamDetailSerializer",
]
