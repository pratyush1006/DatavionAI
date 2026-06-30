"""
API views for Permission.
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
    PermissionCreateSerializer,
    PermissionDetailSerializer,
    PermissionListSerializer,
    PermissionUpdateSerializer,
)
from apps.rbac.selectors import (
    get_permission_by_id,
    get_permissions,
)
from apps.rbac.services import (
    create_permission,
    delete_permission,
    update_permission,
)


@extend_schema(tags=["RBAC"])
class PermissionListCreateAPIView(BaseListCreateAPIView):
    """
    List and create permissions.
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
        return get_permissions()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PermissionCreateSerializer
        return PermissionListSerializer

    def perform_create(self, serializer):
        self.instance = create_permission(
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

        output_serializer = PermissionDetailSerializer(
            self.instance,
            context=self.get_serializer_context(),
        )

        return self.created_response(
            data=output_serializer.data,
        )


@extend_schema(tags=["RBAC"])
class PermissionRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete permissions.
    """

    permission_classes = (IsAuthenticated,)

    lookup_url_kwarg = "permission_id"

    def get_object(self):
        return get_permission_by_id(
            permission_id=self.kwargs["permission_id"],
        )

    def get_serializer_class(self):
        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return PermissionUpdateSerializer

        return PermissionDetailSerializer

    def perform_update(self, serializer):
        self.instance = update_permission(
            instance=self.get_object(),
            validated_data=serializer.validated_data,
        )

    def perform_destroy(self, instance):
        delete_permission(
            instance=instance,
        )
