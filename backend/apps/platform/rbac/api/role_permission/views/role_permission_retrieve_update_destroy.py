"""
Role permission retrieve/update/destroy API view.

Handles:

- Retrieve role permission
- Update role permission
- Delete role permission
- RBAC authorization
- Audit integration through services
"""

from __future__ import annotations

from typing import TYPE_CHECKING

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

if TYPE_CHECKING:
    from apps.platform.rbac.models import RolePermission


@extend_schema(
    tags=[
        "RBAC - Role Permissions",
    ],
)
class RolePermissionRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update, and delete role permission assignments.

    Flow:

        API
         |
        Serializer
         |
        Service
         |
        Validator
         |
        Model
         |
        AuditLog
    """

    queryset = None

    lookup_field = "id"

    # =========================================================================
    # Services
    # =========================================================================

    update_service = staticmethod(
        update_role_permission,
    )

    delete_service = staticmethod(
        delete_role_permission,
    )

    # =========================================================================
    # Object retrieval
    # =========================================================================

    def get_object(
        self,
    ) -> RolePermission:
        """
        Return role permission instance.
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
        Return serializer by action.
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

    permission_classes_map = {
        "GET": (CanViewRolePermission,),
        "PUT": (CanUpdateRolePermission,),
        "PATCH": (CanUpdateRolePermission,),
        "DELETE": (CanDeleteRolePermission,),
    }


__all__ = [
    "RolePermissionRetrieveUpdateDestroyAPIView",
]
