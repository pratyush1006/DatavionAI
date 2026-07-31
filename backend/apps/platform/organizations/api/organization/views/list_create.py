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
from apps.platform.organizations.api.organization.serializers import (
    OrganizationCreateSerializer,
    OrganizationDetailSerializer,
    OrganizationListSerializer,
)
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.organizations.permissions.organization import (
    CanCreateOrganization,
    CanViewOrganization,
)
from apps.platform.organizations.selectors import (
    get_organizations,
)
from apps.platform.organizations.services import (
    create_organization,
)

ORGANIZATION_TAG: Final[tuple[str, ...]] = ("Organizations",)


@extend_schema(
    tags=ORGANIZATION_TAG,
)
class OrganizationListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    API endpoint for listing and creating organizations.

    GET
        Returns organizations visible to the current user.

    POST
        Creates a new organization through the Organization
        service layer.
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

    create_service = staticmethod(
        create_organization,
    )

    create_success_message = "Organization created successfully."

    search_fields = (
        "name",
        "display_name",
        "code",
        "city",
        "state",
        "country",
    )

    ordering = ("name",)

    ordering_fields = (
        "name",
        "display_name",
        "code",
        "city",
        "created_at",
        "updated_at",
    )

    filterset_fields = (
        "category",
        "organization_type",
        "status",
        "verification_status",
        "subscription_status",
        "country",
    )

    def get_queryset(
        self,
    ) -> QuerySet[Organization]:
        """
        Return organizations visible to the current request.

        Read operations are delegated to the selector layer.
        """

        return get_organizations()


__all__: tuple[str, ...] = ("OrganizationListCreateAPIView",)
