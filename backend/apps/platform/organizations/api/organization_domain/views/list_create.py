"""
API views for listing and creating organization domains.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.organizations.api.organization_domain.serializers import (
    OrganizationDomainCreateSerializer,
    OrganizationDomainDetailSerializer,
    OrganizationDomainListSerializer,
)
from apps.platform.organizations.models import (
    OrganizationDomain,
)
from apps.platform.organizations.permissions.organization_domain import (
    CanCreateOrganizationDomain,
    CanViewOrganizationDomain,
)
from apps.platform.organizations.selectors import (
    get_organization_domains,
)
from apps.platform.organizations.services import (
    create_organization_domain,
)

ORGANIZATION_DOMAIN_TAG: Final[tuple[str, ...]] = ("Organization Domains",)


@extend_schema(
    tags=ORGANIZATION_DOMAIN_TAG,
)
class OrganizationDomainListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing organization domains or create a new domain.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizationDomain,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateOrganizationDomain,
        ),
    }

    serializer_classes = {
        "GET": OrganizationDomainListSerializer,
        "POST": OrganizationDomainCreateSerializer,
    }

    detail_serializer_class = OrganizationDomainDetailSerializer

    create_service = staticmethod(
        create_organization_domain,
    )

    create_success_message = "Organization domain created successfully."

    search_fields = (
        "domain",
        "organization__name",
    )

    ordering = ("domain",)

    ordering_fields = (
        "domain",
        "domain_type",
        "verification_status",
        "is_primary",
        "ssl_enabled",
        "created_at",
        "updated_at",
    )

    filterset_fields = (
        "organization",
        "domain_type",
        "verification_status",
        "is_primary",
        "ssl_enabled",
    )

    def get_queryset(
        self,
    ) -> QuerySet[OrganizationDomain]:
        """
        Return organization domains.
        """

        return get_organization_domains()


__all__: tuple[str, ...] = ("OrganizationDomainListCreateAPIView",)
