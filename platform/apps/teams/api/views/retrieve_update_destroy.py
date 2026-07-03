"""
API views for retrieving, updating and deleting teams.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.teams.api.serializers import (
    TeamDetailSerializer,
    TeamUpdateSerializer,
)
from apps.teams.permissions import (
    CanDeleteTeam,
    CanUpdateTeam,
    CanViewTeam,
)
from apps.teams.selectors import get_team_by_id
from apps.teams.services import (
    delete_team,
    update_team,
)

TEAM_TAG: Final[tuple[str, ...]] = ("Teams",)


@extend_schema(tags=TEAM_TAG)
class TeamRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a team.
    """

    lookup_url_kwarg = "team_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewTeam,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateTeam,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateTeam,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteTeam,
        ),
    }

    serializer_classes = {
        "GET": TeamDetailSerializer,
        "PUT": TeamUpdateSerializer,
        "PATCH": TeamUpdateSerializer,
    }

    detail_serializer_class = TeamDetailSerializer

    update_service = update_team

    delete_service = delete_team

    update_success_message = "Team updated successfully."

    def get_object(self):
        """
        Return the requested team.
        """

        return get_team_by_id(
            team_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "TeamRetrieveUpdateDestroyAPIView",
]
