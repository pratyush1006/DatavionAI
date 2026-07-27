"""
List/Create API view for Organization Module.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import BaseListCreateAPIView
from apps.platform.organizations.api.organization_module.serializers import (
    OrganizationModuleCreateSerializer,
    OrganizationModuleDetailSerializer,
    OrganizationModuleListSerializer,
)
from apps.platform.organizations.permissions.organization_module import (
    CanCreateOrganizationModule,
    CanViewOrganizationModule,
)
from apps.platform.organizations.selectors.organization_module import (
    get_organization_modules,
)
from apps.platform.organizations.services.organization_module import (
    create_organization_module,
)


@extend_schema(
    tags=["Organization Modules"],
)
class OrganizationModuleListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create organization module entitlements.
    """

    permission_classes = (IsAuthenticated,)

    permission_classes_map = {
        "GET": (CanViewOrganizationModule,),
        "POST": (CanCreateOrganizationModule,),
    }

    serializer_classes = {
        "GET": OrganizationModuleListSerializer,
        "POST": OrganizationModuleCreateSerializer,
    }

    detail_serializer_class = OrganizationModuleDetailSerializer

    create_service = staticmethod(
        create_organization_module,
    )

    search_fields = ("module_code",)

    ordering = ("module_code",)

    ordering_fields = (
        "module_code",
        "status",
        "enabled_at",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "module_code",
        "status",
    )

    def get_queryset(self):
        return get_organization_modules()
