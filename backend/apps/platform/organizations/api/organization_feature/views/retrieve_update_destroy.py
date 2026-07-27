"""
API views for retrieving, updating and deleting organization features.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.organizations.api.organization_feature.serializers import (
    OrganizationFeatureDetailSerializer,
    OrganizationFeatureUpdateSerializer,
)
from apps.platform.organizations.permissions.organization_feature import (
    CanDeleteOrganizationFeature,
    CanUpdateOrganizationFeature,
    CanViewOrganizationFeature,
)
from apps.platform.organizations.selectors import (
    get_organization_feature,
)
from apps.platform.organizations.services import (
    delete_organization_feature,
    update_organization_feature,
)

ORGANIZATION_FEATURE_TAG: Final[tuple[str, ...]] = ("Organization Features",)


@extend_schema(
    tags=ORGANIZATION_FEATURE_TAG,
)
class OrganizationFeatureRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete an organization feature.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizationFeature,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateOrganizationFeature,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateOrganizationFeature,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteOrganizationFeature,
        ),
    }

    serializer_classes = {
        "GET": OrganizationFeatureDetailSerializer,
        "PUT": OrganizationFeatureUpdateSerializer,
        "PATCH": OrganizationFeatureUpdateSerializer,
    }

    detail_serializer_class = OrganizationFeatureDetailSerializer

    update_service = staticmethod(
        update_organization_feature,
    )

    delete_service = staticmethod(
        delete_organization_feature,
    )

    update_success_message = "Organization feature updated successfully."

    delete_success_message = "Organization feature deleted successfully."

    def get_object(
        self,
    ):
        """
        Return the requested organization feature.
        """

        return get_organization_feature(
            pk=self.kwargs["pk"],
        )


__all__: tuple[str, ...] = ("OrganizationFeatureRetrieveUpdateDestroyAPIView",)
