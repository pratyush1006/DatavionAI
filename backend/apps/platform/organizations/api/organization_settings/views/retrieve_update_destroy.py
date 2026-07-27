"""
API views for retrieving, updating, and deleting organization settings.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.organizations.api.organization_settings.serializers import (
    OrganizationSettingsDetailSerializer,
    OrganizationSettingsUpdateSerializer,
)
from apps.platform.organizations.models import (
    OrganizationSettings,
)
from apps.platform.organizations.permissions.organization_settings import (
    CanDeleteOrganizationSettings,
    CanUpdateOrganizationSettings,
    CanViewOrganizationSettings,
)
from apps.platform.organizations.selectors import (
    get_organization_settings_by_id,
)
from apps.platform.organizations.services import (
    delete_organization_settings,
    update_organization_settings,
)

ORGANIZATION_SETTINGS_TAG: Final[tuple[str, ...]] = ("Organization Settings",)


@extend_schema(
    tags=ORGANIZATION_SETTINGS_TAG,
)
class OrganizationSettingsRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, or delete organization settings.
    """

    lookup_url_kwarg = "settings_id"

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizationSettings,
        ),
        "PUT": (
            IsAuthenticated,
            CanUpdateOrganizationSettings,
        ),
        "PATCH": (
            IsAuthenticated,
            CanUpdateOrganizationSettings,
        ),
        "DELETE": (
            IsAuthenticated,
            CanDeleteOrganizationSettings,
        ),
    }

    serializer_classes = {
        "GET": OrganizationSettingsDetailSerializer,
        "PUT": OrganizationSettingsUpdateSerializer,
        "PATCH": OrganizationSettingsUpdateSerializer,
    }

    detail_serializer_class = OrganizationSettingsDetailSerializer

    update_service = staticmethod(
        update_organization_settings,
    )

    delete_service = staticmethod(
        delete_organization_settings,
    )

    update_success_message = "Organization settings updated successfully."

    delete_success_message = "Organization settings deleted successfully."

    def get_object(
        self,
    ) -> OrganizationSettings:
        """
        Return the requested settings record.
        """

        return get_organization_settings_by_id(
            settings_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__: tuple[str, ...] = ("OrganizationSettingsRetrieveUpdateDestroyAPIView",)
