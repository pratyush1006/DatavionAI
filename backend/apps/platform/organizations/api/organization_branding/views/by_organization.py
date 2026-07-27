"""
API view for retrieving organization branding by organization.
"""

from __future__ import annotations

from typing import Final
from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.platform.organizations.api.organization_branding.serializers import (
    OrganizationBrandingDetailSerializer,
)
from apps.platform.organizations.permissions.organization_branding import (
    CanViewOrganizationBranding,
)
from apps.platform.organizations.selectors import (
    get_organization_branding_by_organization,
)

ORGANIZATION_BRANDING_TAG: Final[tuple[str, ...]] = ("Organization Branding",)


@extend_schema(
    tags=ORGANIZATION_BRANDING_TAG,
    responses=OrganizationBrandingDetailSerializer,
)
class OrganizationBrandingByOrganizationAPIView(
    APIView,
):
    """
    Retrieve the branding configuration for an organization.
    """

    permission_classes = (
        IsAuthenticated,
        CanViewOrganizationBranding,
    )

    def get(
        self,
        request: Request,
        organization_id: UUID,
    ) -> Response:
        """
        Return the branding configuration for an organization.
        """

        branding = get_organization_branding_by_organization(
            organization_id=organization_id,
        )

        if branding is None:
            raise Http404(
                "Organization branding does not exist.",
            )

        serializer = OrganizationBrandingDetailSerializer(
            branding,
        )

        return Response(
            serializer.data,
        )


__all__: tuple[str, ...] = ("OrganizationBrandingByOrganizationAPIView",)
