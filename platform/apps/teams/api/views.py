from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.rbac.permissions import (
    CanAddTeams,
    CanChangeTeams,
    CanDeleteTeams,
    CanViewTeams,
)
from apps.teams.selectors import (
    get_team_by_id,
    get_teams,
)
from apps.teams.serializers import (
    TeamCreateSerializer,
    TeamDetailSerializer,
    TeamListSerializer,
    TeamUpdateSerializer,
)
from apps.teams.services import (
    create_team,
    delete_team,
    update_team,
)


class TeamListCreateAPIView(BaseListCreateAPIView):
    """
    GET -> List Teams
    POST -> Create Team
    """

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

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
        "is_active",
    )

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated,
                CanViewTeams,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
                CanAddTeams,
            ]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return get_teams()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TeamCreateSerializer

        return TeamListSerializer

    @extend_schema(tags=["Teams"])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(tags=["Teams"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        team = create_team(serializer.validated_data.copy())

        return Response(
            TeamDetailSerializer(team).data,
            status=status.HTTP_201_CREATED,
        )


class TeamRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    """
    GET
    PUT
    PATCH
    DELETE
    """

    lookup_url_kwarg = "team_id"

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated,
                CanViewTeams,
            ]

        elif self.request.method in (
            "PUT",
            "PATCH",
        ):
            permission_classes = [
                IsAuthenticated,
                CanChangeTeams,
            ]

        else:
            permission_classes = [
                IsAuthenticated,
                CanDeleteTeams,
            ]

        return [permission() for permission in permission_classes]

    def get_object(self):
        return get_team_by_id(self.kwargs["team_id"])

    def get_serializer_class(self):
        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return TeamUpdateSerializer

        return TeamDetailSerializer

    @extend_schema(tags=["Teams"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(tags=["Teams"])
    def patch(self, request, *args, **kwargs):
        team = self.get_object()

        serializer = self.get_serializer(
            team,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        team = update_team(
            team,
            serializer.validated_data.copy(),
        )

        return Response(TeamDetailSerializer(team).data)

    @extend_schema(tags=["Teams"])
    def put(self, request, *args, **kwargs):
        team = self.get_object()

        serializer = self.get_serializer(
            team,
            data=request.data,
            partial=False,
        )

        serializer.is_valid(raise_exception=True)

        team = update_team(
            team,
            serializer.validated_data.copy(),
        )

        return Response(TeamDetailSerializer(team).data)

    @extend_schema(tags=["Teams"])
    def delete(self, request, *args, **kwargs):
        team = self.get_object()

        delete_team(team)

        return Response(status=status.HTTP_204_NO_CONTENT)
