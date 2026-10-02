"""
API views for retrieving, updating, and deleting organization hierarchies.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.organizations.api.organization_hierarchy.serializers import (
    OrganizationHierarchyDetailSerializer,
    OrganizationHierarchyUpdateSerializer,
)
from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from apps.platform.organizations.permissions.organization_hierarchy import (
    CanDeleteOrganizationHierarchy,
    CanUpdateOrganizationHierarchy,
    CanViewOrganizationHierarchy,
)
from apps.platform.organizations.selectors import (
    get_organization_hierarchy_by_id,
)
from apps.platform.organizations.services import (
    delete_organization_hierarchy,
    update_organization_hierarchy,
)

ORGANIZATION_HIERARCHY_TAG: Final = "Organization Hierarchies"


@extend_schema(
    tags=[ORGANIZATION_HIERARCHY_TAG],
)
class OrganizationHierarchyRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete an organization hierarchy.
    """

    lookup_url_kwarg = "hierarchy_id"

    update_service = staticmethod(
        update_organization_hierarchy,
    )

    delete_service = staticmethod(
        delete_organization_hierarchy,
    )

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizationHierarchy,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateOrganizationHierarchy,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateOrganizationHierarchy,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteOrganizationHierarchy,
        ),
    }

    serializer_classes = {
        "GET": OrganizationHierarchyDetailSerializer,
        "PUT": OrganizationHierarchyUpdateSerializer,
        "PATCH": OrganizationHierarchyUpdateSerializer,
    }

    detail_serializer_class = OrganizationHierarchyDetailSerializer

    update_success_message = "Organization hierarchy updated successfully."

    delete_success_message = "Organization hierarchy deleted successfully."

    def get_object(
        self,
    ) -> OrganizationHierarchy:
        """
        Return the requested organization hierarchy.
        """

        return get_organization_hierarchy_by_id(
            hierarchy_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__: tuple[str, ...] = ("OrganizationHierarchyRetrieveUpdateDestroyAPIView",)
