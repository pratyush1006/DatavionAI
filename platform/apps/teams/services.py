from apps.teams.models import Team


def create_team(
    validated_data: dict,
) -> Team:
    """
    Create a new team.
    """

    team = Team.objects.create(**validated_data)

    return team


def update_team(
    team: Team,
    validated_data: dict,
) -> Team:
    """
    Update an existing team.
    """

    for field, value in validated_data.items():
        setattr(
            team,
            field,
            value,
        )

    team.save()

    return team


def delete_team(
    team: Team,
) -> None:
    """
    Delete a team.
    """

    team.delete()
