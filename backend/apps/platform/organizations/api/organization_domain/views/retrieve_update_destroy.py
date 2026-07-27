"""
API view for retrieving, updating and deleting organization domains.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.organizations.api.organization_domain.serializers import (
    OrganizationDomainDetailSerializer,
    OrganizationDomainUpdateSerializer,
)
from apps.platform.organizations.permissions.organization_domain import (
    CanDeleteOrganizationDomain,
    CanUpdateOrganizationDomain,
    CanViewOrganizationDomain,
)
from apps.platform.organizations.selectors import (
    get_organization_domain,
)
from apps.platform.organizations.services import (
    delete_organization_domain,
    update_organization_domain,
)

ORGANIZATION_DOMAIN_TAG: Final[tuple[str, ...]] = ("Organization Domains",)


@extend_schema(
    tags=ORGANIZATION_DOMAIN_TAG,
)
class OrganizationDomainRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete an organization domain.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizationDomain,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateOrganizationDomain,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateOrganizationDomain,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteOrganizationDomain,
        ),
    }

    serializer_classes = {
        "GET": OrganizationDomainDetailSerializer,
        "PUT": OrganizationDomainUpdateSerializer,
        "PATCH": OrganizationDomainUpdateSerializer,
    }

    detail_serializer_class = OrganizationDomainDetailSerializer

    update_service = staticmethod(
        update_organization_domain,
    )

    delete_service = staticmethod(
        delete_organization_domain,
    )

    update_success_message = "Organization domain updated successfully."

    delete_success_message = "Organization domain deleted successfully."

    def get_object(
        self,
    ):
        """
        Return the requested organization domain.
        """

        return get_organization_domain(
            pk=self.kwargs["pk"],
        )


__all__: tuple[str, ...] = ("OrganizationDomainRetrieveUpdateDestroyAPIView",)
