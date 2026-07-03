"""
Business services for the Teams app.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.db import transaction

from apps.teams.models import Team

type TeamData = Mapping[str, object]


@transaction.atomic
def create_team(
    *,
    validated_data: TeamData,
) -> Team:
    """
    Create a new team.
    """

    return Team.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_team(
    *,
    instance: Team,
    validated_data: TeamData,
) -> Team:
    """
    Update an existing team.
    """

    if not validated_data:
        return instance

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save(
        update_fields=tuple(validated_data.keys()),
    )

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_team(
    *,
    instance: Team,
) -> None:
    """
    Delete a team.
    """

    instance.delete()
