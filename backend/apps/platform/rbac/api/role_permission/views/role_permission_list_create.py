"""
Role permission list/create API view.

RBAC role permission management endpoint.
"""

from __future__ import annotations

from drf_spectacular.utils import (
    extend_schema,
)

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.rbac.api.role_permission.serializers import (
    RolePermissionCreateSerializer,
    RolePermissionListSerializer,
)
from apps.platform.rbac.permissions import (
    CanCreateRolePermission,
    CanViewRolePermission,
)
from apps.platform.rbac.selectors import (
    get_role_permissions,
)


@extend_schema(
    tags=[
        "RBAC - Role Permissions",
    ],
)
class RolePermissionListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create role permission assignments.

    Supports:

    - Permission assignment
    - Permission listing
    - RBAC authorization
    - Audit integration through services
    """

    # =========================================================================
    # Queryset
    # =========================================================================

    queryset = get_role_permissions()

    def get_queryset(
        self,
    ):
        """
        Return optimized queryset.
        """

        return get_role_permissions()

    # =========================================================================
    # Serializer
    # =========================================================================

    def get_serializer_class(
        self,
    ):
        """
        Return serializer based on HTTP method.
        """

        if self.request.method == "POST":
            return RolePermissionCreateSerializer

        return RolePermissionListSerializer

    # =========================================================================
    # Permissions
    # =========================================================================

    permission_classes_map = {
        "GET": (CanViewRolePermission,),
        "POST": (CanCreateRolePermission,),
    }


__all__ = [
    "RolePermissionListCreateAPIView",
]
