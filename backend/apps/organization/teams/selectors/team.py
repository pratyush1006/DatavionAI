"""
Team selectors.

Read/query operations for teams.
"""

from __future__ import annotations

from uuid import UUID

from apps.organization.teams.models import (
    Team,
)
from django.db import models
from django.db.models import QuerySet


class TeamSelector:
    """
    Team query services.
    """

    @staticmethod
    def list(
        *,
        organization_id: UUID,
    ) -> QuerySet[Team]:
        """
        List organization teams.
        """

        return (
            Team.objects.filter(
                organization_id=organization_id,
            )
            .select_related(
                "organization",
            )
            .prefetch_related(
                "roles",
                "members",
                "department_assignments__department",
            )
            .order_by(
                "name",
            )
        )

    @staticmethod
    def get(
        *,
        team_id: UUID,
    ) -> Team:
        """
        Get team by ID.
        """

        return (
            Team.objects.select_related(
                "organization",
            )
            .prefetch_related(
                "roles",
                "members",
                "department_assignments__department",
            )
            .get(
                id=team_id,
            )
        )

    @staticmethod
    def active(
        *,
        organization_id: UUID,
    ) -> QuerySet[Team]:
        """
        List active teams.
        """

        return (
            Team.objects.filter(
                organization_id=organization_id,
                is_active=True,
            )
            .select_related(
                "organization",
            )
            .order_by(
                "name",
            )
        )

    @staticmethod
    def search(
        *,
        organization_id: UUID,
        query: str,
    ) -> QuerySet[Team]:
        """
        Search teams by name or code.
        """

        return (
            Team.objects.filter(
                organization_id=organization_id,
            )
            .filter(
                models.Q(
                    name__icontains=query,
                )
                | models.Q(
                    code__icontains=query,
                )
            )
            .select_related(
                "organization",
            )
            .order_by(
                "name",
            )
        )


# ============================================================
# Backward compatibility selectors
# ============================================================


def get_teams(
    *,
    organization_id: UUID,
):
    """
    Legacy wrapper.

    Return organization teams.
    """

    return TeamSelector.list(
        organization_id=organization_id,
    )


def get_team(
    *,
    team_id: UUID,
):
    """
    Legacy wrapper.

    Return single team.
    """

    return TeamSelector.get(
        team_id=team_id,
    )


def get_team_by_id(
    *,
    team_id: UUID,
):
    """
    Alias for get_team.
    """

    return TeamSelector.get(
        team_id=team_id,
    )


def get_active_teams(
    *,
    organization_id: UUID,
):
    """
    Return active teams.
    """

    return TeamSelector.active(
        organization_id=organization_id,
    )


__all__ = (
    "TeamSelector",
    "get_teams",
    "get_team",
    "get_team_by_id",
    "get_active_teams",
)
