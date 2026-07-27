"""
API views for retrieving, updating, and deleting organization branding records.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.organizations.api.organization_branding.serializers import (
    OrganizationBrandingDetailSerializer,
    OrganizationBrandingUpdateSerializer,
)
from apps.platform.organizations.models import (
    OrganizationBranding,
)
from apps.platform.organizations.permissions.organization_branding import (
    CanDeleteOrganizationBranding,
    CanUpdateOrganizationBranding,
    CanViewOrganizationBranding,
)
from apps.platform.organizations.selectors import (
    get_organization_branding_by_id,
)
from apps.platform.organizations.services import (
    delete_organization_branding,
    update_organization_branding,
)

ORGANIZATION_BRANDING_TAG: Final[tuple[str, ...]] = ("Organization Branding",)


@extend_schema(
    tags=ORGANIZATION_BRANDING_TAG,
)
class OrganizationBrandingRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete an organization branding record.
    """

    lookup_url_kwarg = "branding_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizationBranding,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateOrganizationBranding,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateOrganizationBranding,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteOrganizationBranding,
        ),
    }

    serializer_classes = {
        "GET": OrganizationBrandingDetailSerializer,
        "PUT": OrganizationBrandingUpdateSerializer,
        "PATCH": OrganizationBrandingUpdateSerializer,
    }

    detail_serializer_class = OrganizationBrandingDetailSerializer

    update_service = staticmethod(
        update_organization_branding,
    )

    delete_service = staticmethod(
        delete_organization_branding,
    )

    update_success_message = "Organization branding updated successfully."

    delete_success_message = "Organization branding deleted successfully."

    def get_object(
        self,
    ) -> OrganizationBranding:
        """
        Return the requested branding record.
        """

        return get_organization_branding_by_id(
            branding_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__: tuple[str, ...] = ("OrganizationBrandingRetrieveUpdateDestroyAPIView",)
