from django.shortcuts import get_object_or_404

from apps.teams.models import Team


def get_teams():
    """
    Return all teams ordered by name.
    """

    return Team.objects.select_related(
        "department",
        "department__organization",
    ).order_by("name")


def get_team_by_id(
    team_id: int,
) -> Team:
    """
    Return a team by ID.
    """

    return get_object_or_404(
        Team.objects.select_related(
            "department",
            "department__organization",
        ),
        id=team_id,
    )
