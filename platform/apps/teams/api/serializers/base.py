"""
Base serializer for the Teams application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.teams.models import Team


class TeamBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for Team.
    """

    class Meta:
        model = Team
        fields = "__all__"


__all__ = [
    "TeamBaseSerializer",
]
