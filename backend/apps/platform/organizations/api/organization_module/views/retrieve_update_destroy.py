"""
Retrieve/Update/Delete API view for Organization Module.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.organizations.api.organization_module.serializers import (
    OrganizationModuleDetailSerializer,
    OrganizationModuleUpdateSerializer,
)
from apps.platform.organizations.permissions.organization_module import (
    CanDeleteOrganizationModule,
    CanUpdateOrganizationModule,
    CanViewOrganizationModule,
)
from apps.platform.organizations.selectors.organization_module import (
    get_organization_module,
)
from apps.platform.organizations.services.organization_module import (
    delete_organization_module,
    update_organization_module,
)


@extend_schema(
    tags=["Organization Modules"],
)
class OrganizationModuleRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete organization module entitlements.
    """

    permission_classes = (IsAuthenticated,)

    permission_classes_map = {
        "GET": (CanViewOrganizationModule,),
        "PUT": (CanUpdateOrganizationModule,),
        "PATCH": (CanUpdateOrganizationModule,),
        "DELETE": (CanDeleteOrganizationModule,),
    }

    serializer_classes = {
        "GET": OrganizationModuleDetailSerializer,
        "PUT": OrganizationModuleUpdateSerializer,
        "PATCH": OrganizationModuleUpdateSerializer,
    }

    detail_serializer_class = OrganizationModuleDetailSerializer

    update_service = staticmethod(
        update_organization_module,
    )

    delete_service = staticmethod(
        delete_organization_module,
    )

    update_success_message = "Organization module updated successfully."

    delete_success_message = "Organization module deleted successfully."

    def get_object(self):
        return get_organization_module(
            self.kwargs["pk"],
        )
