"""
Role hierarchy list/create API views.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
)
from apps.platform.rbac.api.role_hierarchy.serializers import (
    RoleHierarchyCreateSerializer,
    RoleHierarchyListSerializer,
)
from apps.platform.rbac.permissions import (
    CanCreateRoleHierarchy,
    CanViewRoleHierarchy,
)
from apps.platform.rbac.selectors import (
    get_role_hierarchies,
)
from apps.platform.rbac.services import (
    create_role_hierarchy,
)


class RoleHierarchyListCreateAPIView(
    BaseListCreateAPIView,
):
    """
    List and create role hierarchies.
    """

    queryset = get_role_hierarchies()

    permission_classes = [
        CanViewRoleHierarchy,
    ]

    create_permission_classes = [
        CanCreateRoleHierarchy,
    ]

    list_serializer_class = RoleHierarchyListSerializer

    create_serializer_class = RoleHierarchyCreateSerializer

    create_service = staticmethod(create_role_hierarchy)


__all__ = [
    "RoleHierarchyListCreateAPIView",
]
