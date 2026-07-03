"""
API views for retrieving, updating, and deleting organizations.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.organizations.api.serializers import (
    OrganizationDetailSerializer,
    OrganizationUpdateSerializer,
)
from apps.organizations.permissions.organization import (
    CanDeleteOrganization,
    CanUpdateOrganization,
    CanViewOrganization,
)
from apps.organizations.selectors import get_organization_by_id
from apps.organizations.services import (
    delete_organization,
    update_organization,
)

ORGANIZATION_TAG: Final[tuple[str, ...]] = ("Organizations",)


@extend_schema(tags=ORGANIZATION_TAG)
class OrganizationRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an organization.
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

    update_service = update_organization

    delete_service = delete_organization

    update_success_message = "Organization updated successfully."

    def get_object(self):
        """
        Return the requested organization.
        """

        return get_organization_by_id(
            organization_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "OrganizationRetrieveUpdateDestroyAPIView",
]
