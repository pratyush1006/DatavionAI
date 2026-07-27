"""
API views for listing and creating organization features.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.organizations.api.organization_feature.serializers import (
    OrganizationFeatureCreateSerializer,
    OrganizationFeatureDetailSerializer,
    OrganizationFeatureListSerializer,
)
from apps.platform.organizations.models import (
    OrganizationFeature,
)
from apps.platform.organizations.permissions.organization_feature import (
    CanCreateOrganizationFeature,
    CanViewOrganizationFeature,
)
from apps.platform.organizations.selectors import (
    get_organization_features,
)
from apps.platform.organizations.services import (
    create_organization_feature,
)

ORGANIZATION_FEATURE_TAG: Final[tuple[str, ...]] = ("Organization Features",)


@extend_schema(
    tags=ORGANIZATION_FEATURE_TAG,
)
class OrganizationFeatureListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing organization features or create a new feature entitlement.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizationFeature,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateOrganizationFeature,
        ),
    }

    serializer_classes = {
        "GET": OrganizationFeatureListSerializer,
        "POST": OrganizationFeatureCreateSerializer,
    }

    detail_serializer_class = OrganizationFeatureDetailSerializer

    create_service = staticmethod(
        create_organization_feature,
    )

    create_success_message = "Organization feature created successfully."

    search_fields = (
        "organization__name",
        "feature_code",
    )

    ordering = ("feature_code",)

    ordering_fields = (
        "feature_code",
        "status",
        "enabled_at",
        "disabled_at",
        "created_at",
        "updated_at",
    )

    filterset_fields = (
        "organization",
        "feature_code",
        "status",
    )

    def get_queryset(
        self,
    ) -> QuerySet[OrganizationFeature]:
        """
        Return organization feature entitlements.
        """

        return get_organization_features()


__all__: tuple[str, ...] = ("OrganizationFeatureListCreateAPIView",)
