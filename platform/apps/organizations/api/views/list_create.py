"""
API views for listing and creating organizations.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.organizations.api.serializers import (
    OrganizationCreateSerializer,
    OrganizationDetailSerializer,
    OrganizationListSerializer,
)
from apps.organizations.models import Organization
from apps.organizations.permissions.organization import (
    CanCreateOrganization,
    CanViewOrganization,
)
from apps.organizations.selectors import get_organizations
from apps.organizations.services import create_organization

ORGANIZATION_TAG: Final[tuple[str, ...]] = ("Organizations",)


@extend_schema(
    tags=ORGANIZATION_TAG,
)
class OrganizationListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing organizations or create a new organization.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganization,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateOrganization,
        ),
    }

    serializer_classes = {
        "GET": OrganizationListSerializer,
        "POST": OrganizationCreateSerializer,
    }

    detail_serializer_class = OrganizationDetailSerializer

    create_service = create_organization

    create_success_message = "Organization created successfully."

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

    def get_queryset(
        self,
    ) -> QuerySet[Organization]:
        """
        Return the organizations queryset.
        """

        return get_organizations()


__all__ = [
    "OrganizationListCreateAPIView",
]
