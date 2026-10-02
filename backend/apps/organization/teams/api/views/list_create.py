"""
API views for listing and creating teams.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.organization.teams.api.serializers import (
    TeamCreateSerializer,
    TeamDetailSerializer,
    TeamListSerializer,
)
from apps.organization.teams.models import (
    Team,
)
from apps.organization.teams.permissions import (
    CanCreateTeam,
    CanViewTeam,
)
from apps.organization.teams.selectors import (
    get_teams,
)
from apps.organization.teams.workflows import (
    TeamCreationRequest,
    TeamCreationWorkflow,
)

TEAM_TAG: Final[tuple[str, ...]] = ("Teams",)


@extend_schema(
    tags=TEAM_TAG,
)
class TeamListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing teams or create a new team.

    GET:
        Selector driven.

    POST:
        Workflow driven.
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

    create_workflow = TeamCreationWorkflow

    create_success_message = "Team created successfully."

    search_fields = (
        "name",
        "code",
    )

    ordering = ("name",)

    ordering_fields = (
        "name",
        "code",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "is_active",
        "team_type",
        "status",
    )

    def build_workflow_request(
        self,
        validated_data,
    ) -> TeamCreationRequest:
        """
        Build team creation workflow request.
        """

        organization = validated_data["organization"]

        return TeamCreationRequest(
            organization_id=organization.id,
            name=validated_data["name"],
            code=validated_data["code"],
            description=validated_data.get(
                "description",
            ),
            team_type=validated_data.get(
                "team_type",
            ),
        )

    def get_queryset(
        self,
    ) -> QuerySet[Team]:
        """
        Return organization scoped teams.
        """

        organization_id = self.request.query_params.get(
            "organization",
        )

        if organization_id is None:
            organization = getattr(
                self.request,
                "organization",
                None,
            )

            if organization is not None:
                organization_id = organization.id

        if organization_id is None:
            user = self.request.user

            organization_role = user.organization_roles.select_related(
                "organization",
            ).first()

            if organization_role is not None:
                organization_id = organization_role.organization.id

        if organization_id is None:
            return Team.objects.none()

        return get_teams(
            organization_id=organization_id,
        )


__all__ = [
    "TeamListCreateAPIView",
]
