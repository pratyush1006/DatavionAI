"""
API views for listing and creating teams.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.organization.teams.api.serializers import (
    TeamCreateSerializer,
    TeamDetailSerializer,
    TeamListSerializer,
)
from apps.organization.teams.models import Team
from apps.organization.teams.permissions import (
    CanCreateTeam,
    CanViewTeam,
)
from apps.organization.teams.selectors import get_teams
from apps.organization.teams.services import create_team
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TEAM_TAG: Final[tuple[str, ...]] = ("Teams",)


@extend_schema(tags=TEAM_TAG)
class TeamListCreateAPIView(BaseListCreateAPIView):
    """
    List existing teams or create a new team.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewTeam,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateTeam,
        ),
    }

    serializer_classes = {
        "GET": TeamListSerializer,
        "POST": TeamCreateSerializer,
    }

    detail_serializer_class = TeamDetailSerializer

    create_service = create_team

    create_success_message = "Team created successfully."

    search_fields = (
        "name",
        "code",
        "department__name",
        "department__organization__name",
    )

    ordering = ("name",)

    ordering_fields = (
        "name",
        "code",
        "created_at",
    )

    filterset_fields = (
        "department",
        "department__organization",
        "is_active",
    )

    def get_queryset(self) -> QuerySet[Team]:
        """
        Return teams.
        """

        return get_teams()


__all__ = [
    "TeamListCreateAPIView",
]
