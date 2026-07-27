"""
API views for retrieving, updating, and deleting organizations.
"""

from __future__ import annotations

from typing import Final

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.organizations.api.organization.serializers import (
    OrganizationDetailSerializer,
    OrganizationUpdateSerializer,
)
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.organizations.permissions.organization import (
    CanDeleteOrganization,
    CanUpdateOrganization,
    CanViewOrganization,
)
from apps.platform.organizations.selectors import (
    get_organization_by_id,
)
from apps.platform.organizations.services import (
    delete_organization,
    update_organization,
)
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

ORGANIZATION_TAG: Final[tuple[str, ...]] = ("Organizations",)


@extend_schema(
    tags=ORGANIZATION_TAG,
)
class OrganizationRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    API endpoint for retrieving, updating, and deleting organizations.

    GET
        Retrieve organization details.

    PUT/PATCH
        Update an organization through the service layer.

    DELETE
        Archive an organization through the service layer.
    """

    lookup_url_kwarg = "organization_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganization,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateOrganization,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateOrganization,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteOrganization,
        ),
    }

    serializer_classes = {
        "GET": OrganizationDetailSerializer,
        "PUT": OrganizationUpdateSerializer,
        "PATCH": OrganizationUpdateSerializer,
    }

    detail_serializer_class = OrganizationDetailSerializer

    update_service = staticmethod(
        update_organization,
    )

    delete_service = staticmethod(
        delete_organization,
    )

    update_success_message = "Organization updated successfully."

    delete_success_message = "Organization archived successfully."

    def get_object(
        self,
    ) -> Organization:
        """
        Return the organization requested by the URL.

        Retrieval is delegated to the selector layer.
        """

        return get_organization_by_id(
            organization_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__: tuple[str, ...] = ("OrganizationRetrieveUpdateDestroyAPIView",)
