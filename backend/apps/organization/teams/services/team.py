"""
Team services.

Business operations for Team domain.
"""

from __future__ import annotations

from collections.abc import Mapping

from apps.organization.teams.models import (
    Team,
)
from django.db import transaction

type TeamData = Mapping[str, object]


class TeamService:
    """
    Team business service layer.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: TeamData,
    ) -> Team:
        """
        Create a team.
        """

        team = Team(
            **validated_data,
        )

        team.full_clean()

        team.save()

        team.refresh_from_db()

        return team

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Team,
        validated_data: TeamData,
    ) -> Team:
        """
        Update existing team.
        """

        if not validated_data:
            return instance

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save(
            update_fields=tuple(
                validated_data.keys(),
            ),
        )

        instance.refresh_from_db()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Team,
    ) -> Team:
        """
        Delete team.

        Returns deleted instance snapshot
        for workflows/events.
        """

        deleted_team = instance

        instance.delete()

        return deleted_team


def create_team(
    *,
    validated_data: TeamData,
) -> Team:
    """
    Backward compatible create wrapper.
    """

    return TeamService.create(
        validated_data=validated_data,
    )


def update_team(
    *,
    instance: Team,
    validated_data: TeamData,
) -> Team:
    """
    Backward compatible update wrapper.
    """

    return TeamService.update(
        instance=instance,
        validated_data=validated_data,
    )


def delete_team(
    *,
    instance: Team,
) -> Team:
    """
    Backward compatible delete wrapper.
    """

    return TeamService.delete(
        instance=instance,
    )


__all__ = (
    "TeamService",
    "create_team",
    "update_team",
    "delete_team",
)
