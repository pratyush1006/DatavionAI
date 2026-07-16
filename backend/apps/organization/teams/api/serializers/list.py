"""
List serializer for the Teams application.
"""

from __future__ import annotations

from rest_framework import serializers

from .base import TeamBaseSerializer
from .fields import LIST_FIELDS


class TeamListSerializer(TeamBaseSerializer):
    """
    Serializer used for listing teams.
    """

    department = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    organization = serializers.CharField(
        source="department.organization.name",
        read_only=True,
    )

    class Meta(TeamBaseSerializer.Meta):
        fields = (
            *LIST_FIELDS,
            "organization",
        )
        read_only_fields = fields


__all__ = [
    "TeamListSerializer",
]
