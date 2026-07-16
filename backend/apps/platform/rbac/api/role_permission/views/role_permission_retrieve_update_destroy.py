"""
Role permission retrieve/update/destroy API view.
"""

from __future__ import annotations

from drf_spectacular.utils import (
    extend_schema,
)

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.rbac.api.role_permission.serializers import (
    RolePermissionDetailSerializer,
    RolePermissionUpdateSerializer,
)
from apps.platform.rbac.models import (
    RolePermission,
)
from apps.platform.rbac.permissions import (
    CanDeleteRolePermission,
    CanUpdateRolePermission,
    CanViewRolePermission,
)
from apps.platform.rbac.selectors import (
    get_role_permission_by_id,
)
from apps.platform.rbac.services import (
    delete_role_permission,
    update_role_permission,
)


@extend_schema(
    tags=[
        "RBAC - Role Permissions",
    ],
)
class RolePermissionRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    API view for retrieving, updating, and deleting a role permission.
    """

    queryset = RolePermission.objects.none()

    lookup_field = "id"

    # =========================================================================
    # Services
    # =========================================================================

    update_service = staticmethod(update_role_permission)

    delete_service = staticmethod(delete_role_permission)

    # =========================================================================
    # Object
    # =========================================================================

    def get_object(
        self,
    ) -> RolePermission:
        """
        Return the requested role permission.
        """

        return get_role_permission_by_id(
            role_permission_id=self.kwargs[self.lookup_field],
        )

    # =========================================================================
    # Serializer
    # =========================================================================

    def get_serializer_class(
        self,
    ):
        """
        Return the serializer class.
        """

        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return RolePermissionUpdateSerializer

        return RolePermissionDetailSerializer

    # =========================================================================
    # Permissions
    # =========================================================================

    def get_permissions(
        self,
    ):
        """
        Return permission instances.
        """

        permission_map = {
            "GET": [
                CanViewRolePermission,
            ],
            "PUT": [
                CanUpdateRolePermission,
            ],
            "PATCH": [
                CanUpdateRolePermission,
            ],
            "DELETE": [
                CanDeleteRolePermission,
            ],
        }

        permission_classes = permission_map.get(
            self.request.method,
            [],
        )

        return [permission() for permission in permission_classes]


__all__ = [
    "RolePermissionRetrieveUpdateDestroyAPIView",
]
