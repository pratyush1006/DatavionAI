"""
Role permission list/create API view.
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
from apps.platform.rbac.models import (
    RolePermission,
)
from apps.platform.rbac.permissions import (
    CanCreateRolePermission,
    CanViewRolePermission,
)
from apps.platform.rbac.selectors import (
    get_role_permissions,
)
from apps.platform.rbac.services import (
    create_role_permission,
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
    API view for listing and creating role permissions.
    """

    queryset = RolePermission.objects.none()

    # =========================================================================
    # Services
    # =========================================================================

    create_service = staticmethod(create_role_permission)

    # =========================================================================
    # Queryset
    # =========================================================================

    def get_queryset(
        self,
    ):
        """
        Return the role permission queryset.
        """

        return get_role_permissions()

    # =========================================================================
    # Serializers
    # =========================================================================

    def get_serializer_class(
        self,
    ):
        """
        Return the serializer class.
        """

        if self.request.method == "POST":
            return RolePermissionCreateSerializer

        return RolePermissionListSerializer

    # =========================================================================
    # Permissions
    # =========================================================================

    def get_permissions(
        self,
    ):
        """
        Return permission instances.
        """

        if self.request.method == "POST":
            permission_classes = [
                CanCreateRolePermission,
            ]
        else:
            permission_classes = [
                CanViewRolePermission,
            ]

        return [permission() for permission in permission_classes]


__all__ = [
    "RolePermissionListCreateAPIView",
]
