"""
API views for listing and creating organization branding records.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.organizations.api.organization_branding.serializers import (
    OrganizationBrandingCreateSerializer,
    OrganizationBrandingDetailSerializer,
    OrganizationBrandingListSerializer,
)
from apps.platform.organizations.models import (
    OrganizationBranding,
)
from apps.platform.organizations.permissions.organization_branding import (
    CanCreateOrganizationBranding,
    CanViewOrganizationBranding,
)
from apps.platform.organizations.selectors import (
    get_organization_brandings,
)
from apps.platform.organizations.services import (
    create_organization_branding,
)

ORGANIZATION_BRANDING_TAG: Final[tuple[str, ...]] = ("Organization Branding",)


@extend_schema(
    tags=ORGANIZATION_BRANDING_TAG,
)
class OrganizationBrandingListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing organization branding records or create one.
    """

    create_service = staticmethod(
        create_organization_branding,
    )

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizationBranding,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateOrganizationBranding,
        ),
    }

    serializer_classes = {
        "GET": OrganizationBrandingListSerializer,
        "POST": OrganizationBrandingCreateSerializer,
    }

    detail_serializer_class = OrganizationBrandingDetailSerializer

    create_success_message = "Organization branding created successfully."

    search_fields = ("organization__name",)

    ordering = ("organization",)

    ordering_fields = (
        "organization",
        "created_at",
        "updated_at",
    )

    filterset_fields = (
        "organization",
        "theme_mode",
    )

    def get_queryset(
        self,
    ) -> QuerySet[OrganizationBranding]:
        """
        Return branding records visible to the current request.
        """

        return get_organization_brandings()


__all__: tuple[str, ...] = ("OrganizationBrandingListCreateAPIView",)
