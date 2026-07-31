"""
API views for listing and creating organization hierarchies.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.organizations.api.organization_hierarchy.serializers import (
    OrganizationHierarchyCreateSerializer,
    OrganizationHierarchyDetailSerializer,
    OrganizationHierarchyListSerializer,
)
from apps.platform.organizations.models import (
    OrganizationHierarchy,
)
from apps.platform.organizations.permissions.organization_hierarchy import (
    CanCreateOrganizationHierarchy,
    CanViewOrganizationHierarchy,
)
from apps.platform.organizations.selectors import (
    get_organization_hierarchies,
)
from apps.platform.organizations.services import (
    create_organization_hierarchy,
)

ORGANIZATION_HIERARCHY_TAG: Final = "Organization Hierarchies"


@extend_schema(
    tags=[ORGANIZATION_HIERARCHY_TAG],
)
class OrganizationHierarchyListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing organization hierarchies or create a new one.
    """

    create_service = staticmethod(
        create_organization_hierarchy,
    )

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizationHierarchy,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateOrganizationHierarchy,
        ),
    }

    serializer_classes = {
        "GET": OrganizationHierarchyListSerializer,
        "POST": OrganizationHierarchyCreateSerializer,
    }

    detail_serializer_class = OrganizationHierarchyDetailSerializer

    create_success_message = "Organization hierarchy created successfully."

    search_fields = (
        "parent_organization__name",
        "child_organization__name",
    )

    ordering = ("display_order",)

    ordering_fields = (
        "display_order",
        "created_at",
    )

    filterset_fields = (
        "relationship_type",
        "status",
    )

    def get_queryset(
        self,
    ) -> QuerySet[OrganizationHierarchy]:
        """
        Return organization hierarchies.
        """

        return get_organization_hierarchies()


__all__: tuple[str, ...] = ("OrganizationHierarchyListCreateAPIView",)
