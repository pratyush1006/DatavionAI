"""
Organization role detail API views.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.rbac.api.organization_role.serializers import (
    OrganizationRoleDetailSerializer,
    OrganizationRoleUpdateSerializer,
)
from apps.platform.rbac.permissions import (
    CanDeleteOrganizationRole,
    CanUpdateOrganizationRole,
    CanViewOrganizationRole,
)
from apps.platform.rbac.selectors import (
    get_organization_roles,
)
from apps.platform.rbac.services import (
    delete_organization_role,
    update_organization_role,
)


class OrganizationRoleDetailAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete organization roles.
    """

    queryset = get_organization_roles()

    permission_classes = [
        CanViewOrganizationRole,
    ]

    update_permission_classes = [
        CanUpdateOrganizationRole,
    ]

    delete_permission_classes = [
        CanDeleteOrganizationRole,
    ]

    detail_serializer_class = OrganizationRoleDetailSerializer

    update_serializer_class = OrganizationRoleUpdateSerializer

    update_service = update_organization_role

    delete_service = delete_organization_role


__all__ = [
    "OrganizationRoleDetailAPIView",
]
