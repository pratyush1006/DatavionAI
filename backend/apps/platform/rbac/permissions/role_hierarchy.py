"""
Role hierarchy permissions.
"""

from __future__ import annotations

from apps.common.permissions import (
    DatavionPermission,
)


class CanViewRoleHierarchy(
    DatavionPermission,
):
    """
    Permission required to view role hierarchies.
    """

    required_permission = "role_hierarchy.view"


class CanCreateRoleHierarchy(
    DatavionPermission,
):
    """
    Permission required to create role hierarchies.
    """

    required_permission = "role_hierarchy.create"


class CanUpdateRoleHierarchy(
    DatavionPermission,
):
    """
    Permission required to update role hierarchies.
    """

    required_permission = "role_hierarchy.update"


class CanDeleteRoleHierarchy(
    DatavionPermission,
):
    """
    Permission required to delete role hierarchies.
    """

    required_permission = "role_hierarchy.delete"


__all__ = [
    "CanCreateRoleHierarchy",
    "CanDeleteRoleHierarchy",
    "CanUpdateRoleHierarchy",
    "CanViewRoleHierarchy",
]
