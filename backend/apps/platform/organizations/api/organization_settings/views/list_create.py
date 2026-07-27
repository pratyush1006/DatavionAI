"""
API views for listing and creating organization settings.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.organizations.api.organization_settings.serializers import (
    OrganizationSettingsCreateSerializer,
    OrganizationSettingsDetailSerializer,
    OrganizationSettingsListSerializer,
)
from apps.platform.organizations.models import (
    OrganizationSettings,
)
from apps.platform.organizations.permissions.organization_settings import (
    CanCreateOrganizationSettings,
    CanViewOrganizationSettings,
)
from apps.platform.organizations.selectors import (
    get_organization_settings,
)
from apps.platform.organizations.services import (
    create_organization_settings,
)

ORGANIZATION_SETTINGS_TAG: Final[tuple[str, ...]] = ("Organization Settings",)


@extend_schema(
    tags=ORGANIZATION_SETTINGS_TAG,
)
class OrganizationSettingsListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List existing organization settings or create a new record.
    """

    permission_classes_map = {
        "GET": (
            IsAuthenticated,
            CanViewOrganizationSettings,
        ),
        "POST": (
            IsAuthenticated,
            CanCreateOrganizationSettings,
        ),
    }

    serializer_classes = {
        "GET": OrganizationSettingsListSerializer,
        "POST": OrganizationSettingsCreateSerializer,
    }

    detail_serializer_class = OrganizationSettingsDetailSerializer

    create_service = staticmethod(
        create_organization_settings,
    )

    create_success_message = "Organization settings created successfully."

    search_fields = (
        "organization__name",
        "language",
        "timezone",
        "currency",
    )

    ordering = ("organization",)

    ordering_fields = (
        "organization",
        "language",
        "timezone",
        "currency",
        "created_at",
        "updated_at",
    )

    filterset_fields = (
        "language",
        "timezone",
        "currency",
        "mfa_required",
    )

    def get_queryset(
        self,
    ) -> QuerySet[OrganizationSettings]:
        """
        Return organization settings.
        """

        return get_organization_settings()


__all__: tuple[str, ...] = ("OrganizationSettingsListCreateAPIView",)
