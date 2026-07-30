"""
API views for retrieving, updating, and deleting teams.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.organization.teams.api.serializers import (
    TeamDetailSerializer,
    TeamUpdateSerializer,
)
from apps.organization.teams.permissions import (
    CanDeleteTeam,
    CanUpdateTeam,
    CanViewTeam,
)
from apps.organization.teams.selectors import (
    get_team_by_id,
)
from apps.organization.teams.workflows import (
    TeamDeletionRequest,
    TeamDeletionWorkflow,
    TeamUpdateRequest,
    TeamUpdateWorkflow,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

TEAM_TAG: Final[tuple[str, ...]] = ("Teams",)


@extend_schema(
    tags=TEAM_TAG,
)
class TeamRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete a team.

    GET:
        Selector driven.

    PUT/PATCH:
        Workflow driven.

    DELETE:
        Workflow driven.
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

    update_workflow = TeamUpdateWorkflow

    delete_workflow = TeamDeletionWorkflow

    update_success_message = "Team updated successfully."

    delete_success_message = "Team deleted successfully."

    def get_object(
        self,
    ):
        """
        Return requested team.
        """

        return get_team_by_id(
            team_id=self.kwargs[self.lookup_url_kwarg],
        )

    def build_update_workflow_request(
        self,
        instance,
        validated_data,
    ) -> TeamUpdateRequest:
        """
        Build team update workflow request.
        """

        return TeamUpdateRequest(
            team_id=instance.id,
            data=validated_data,
        )

    def build_delete_workflow_request(
        self,
        instance,
    ) -> TeamDeletionRequest:
        """
        Build team deletion workflow request.
        """

        return TeamDeletionRequest(
            team_id=instance.id,
        )


__all__ = [
    "TeamRetrieveUpdateDestroyAPIView",
]
