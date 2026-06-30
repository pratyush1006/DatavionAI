"""
API views for Role.
"""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.rbac.api.serializers import (
    RoleCreateSerializer,
    RoleDetailSerializer,
    RoleListSerializer,
    RoleUpdateSerializer,
)
from apps.rbac.selectors import (
    get_role_by_id,
    get_roles,
)
from apps.rbac.services import (
    create_role,
    delete_role,
    update_role,
)


@extend_schema(tags=["RBAC"])
class RoleListCreateAPIView(BaseListCreateAPIView):
    """
    List and create roles.
    """

    permission_classes = (IsAuthenticated,)

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    search_fields = (
        "name",
        "code",
    )

    ordering_fields = (
        "name",
        "created_at",
    )

    ordering = ("name",)

    def get_queryset(self):
        return get_roles()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return RoleCreateSerializer

        return RoleListSerializer

    def perform_create(self, serializer):
        self.instance = create_role(
            validated_data=serializer.validated_data,
        )

    def create(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        self.perform_create(
            serializer,
        )

        output_serializer = RoleDetailSerializer(
            self.instance,
            context=self.get_serializer_context(),
        )

        return self.created_response(
            data=output_serializer.data,
        )


@extend_schema(tags=["RBAC"])
class RoleRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete roles.
    """

    permission_classes = (IsAuthenticated,)

    lookup_url_kwarg = "role_id"

    def get_object(self):
        return get_role_by_id(
            role_id=self.kwargs["role_id"],
        )

    def get_serializer_class(self):
        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return RoleUpdateSerializer

        return RoleDetailSerializer

    def perform_update(self, serializer):
        self.instance = update_role(
            instance=self.get_object(),
            validated_data=serializer.validated_data,
        )

    def perform_destroy(self, instance):
        delete_role(
            instance=instance,
        )
