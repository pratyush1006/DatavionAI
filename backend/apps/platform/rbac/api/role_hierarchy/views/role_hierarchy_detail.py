"""
Role hierarchy detail API views.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.platform.rbac.api.role_hierarchy.serializers import (
    RoleHierarchyDetailSerializer,
    RoleHierarchyUpdateSerializer,
)
from apps.platform.rbac.permissions import (
    CanDeleteRoleHierarchy,
    CanUpdateRoleHierarchy,
    CanViewRoleHierarchy,
)
from apps.platform.rbac.selectors import (
    get_role_hierarchies,
)
from apps.platform.rbac.services import (
    delete_role_hierarchy,
    update_role_hierarchy,
)


class RoleHierarchyDetailAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update and delete role hierarchies.
    """

    queryset = get_role_hierarchies()

    permission_classes = [
        CanViewRoleHierarchy,
    ]

    update_permission_classes = [
        CanUpdateRoleHierarchy,
    ]

    delete_permission_classes = [
        CanDeleteRoleHierarchy,
    ]

    detail_serializer_class = RoleHierarchyDetailSerializer

    update_serializer_class = RoleHierarchyUpdateSerializer

    update_service = staticmethod(update_role_hierarchy)

    delete_service = staticmethod(delete_role_hierarchy)


__all__ = [
    "RoleHierarchyDetailAPIView",
]
