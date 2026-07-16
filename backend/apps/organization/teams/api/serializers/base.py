"""
Base serializer for the Teams application.
"""

from __future__ import annotations

from apps.organization.teams.models import Team
from rest_framework import serializers


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
