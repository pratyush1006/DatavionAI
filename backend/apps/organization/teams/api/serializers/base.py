"""
Base serializer for Teams application.

Provides common serializer configuration
for Team API serializers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.organization.teams.models import (
    Team,
)

from .fields import (
    DETAIL_FIELDS,
    READ_ONLY_FIELDS,
)


class TeamBaseSerializer(
    serializers.ModelSerializer,
):
    """
    Base serializer for Team.

    Common fields shared across:
    - Create
    - Update
    - List
    - Detail
    """

    class Meta:
        model = Team

        fields = DETAIL_FIELDS

        read_only_fields = (*READ_ONLY_FIELDS,)


__all__ = ("TeamBaseSerializer",)
