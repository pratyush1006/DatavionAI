"""
Organization role list/create API views.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.rbac.api.organization_role.serializers import (
    OrganizationRoleCreateSerializer,
    OrganizationRoleListSerializer,
)
from apps.platform.rbac.permissions import (
    CanCreateOrganizationRole,
    CanViewOrganizationRole,
)
from apps.platform.rbac.selectors import (
    get_organization_roles,
)
from apps.platform.rbac.services import (
    create_organization_role,
)


class OrganizationRoleListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create organization roles.
    """

    queryset = get_organization_roles()

    permission_classes = [
        CanViewOrganizationRole,
    ]

    create_permission_classes = [
        CanCreateOrganizationRole,
    ]

    list_serializer_class = OrganizationRoleListSerializer

    create_serializer_class = OrganizationRoleCreateSerializer

    create_service = create_organization_role


__all__ = [
    "OrganizationRoleListCreateAPIView",
]
