"""
API views for listing and creating organizations.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.common.api.responses import (
    created_response,
)
from apps.organizations.api.serializers import (
    OrganizationCreateSerializer,
    OrganizationDetailSerializer,
    OrganizationListSerializer,
)
from apps.organizations.models import Organization
from apps.organizations.selectors import (
    get_organizations,
)
from apps.organizations.services import (
    create_organization,
)
from apps.rbac.permissions import (
    CanAddOrganizations,
    CanViewOrganizations,
)

ORGANIZATION_TAG: Final = ("Organizations",)


class OrganizationListCreateAPIView(BaseListCreateAPIView):
    """
    List existing organizations or create a new organization.
    """

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    search_fields = (
        "name",
        "code",
        "city",
        "state",
        "country",
    )

    ordering = ("name",)

    ordering_fields = (
        "name",
        "code",
        "city",
        "created_at",
    )

    filterset_fields = (
        "organization_type",
        "country",
        "is_active",
    )

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizations,
        ),
        "POST": (
            IsAuthenticated,
            CanAddOrganizations,
        ),
    }

    def get_permissions(self) -> list[BasePermission]:
        """
        Return permissions based on request method.
        """
        permission_classes = self.permission_classes_map[self.request.method]
        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[Organization]:
        """
        Return organizations queryset.
        """
        return get_organizations()

    def get_serializer_class(self) -> type[BaseSerializer]:
        """
        Return serializer for current request.
        """
        if self.request.method == "POST":
            return OrganizationCreateSerializer

        return OrganizationListSerializer

    @extend_schema(tags=ORGANIZATION_TAG)
    def get(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        List organizations.
        """
        return self.list(
            request,
            *args,
            **kwargs,
        )

    @extend_schema(tags=ORGANIZATION_TAG)
    def post(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Create a new organization.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        organization = create_organization(
            validated_data=serializer.validated_data,
        )

        return created_response(
            data=OrganizationDetailSerializer(
                organization,
            ).data,
            message="Organization created successfully.",
        )
