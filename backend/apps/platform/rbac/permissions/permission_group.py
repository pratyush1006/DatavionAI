"""
RBAC PermissionGroup permission classes.
"""

from __future__ import annotations

from apps.common.permissions import (
    BasePermission,
)


class CanViewPermissionGroup(
    BasePermission,
):
    """
    Permission required to view permission groups.
    """

    required_permission = "rbac.permission_group.view.organization"


class CanCreatePermissionGroup(
    BasePermission,
):
    """
    Permission required to create permission groups.
    """

    required_permission = "rbac.permission_group.create.organization"


class CanUpdatePermissionGroup(
    BasePermission,
):
    """
    Permission required to update permission groups.
    """

    required_permission = "rbac.permission_group.update.organization"


class CanDeletePermissionGroup(
    BasePermission,
):
    """
    Permission required to delete permission groups.
    """

    required_permission = "rbac.permission_group.delete.organization"


__all__ = [
    "CanViewPermissionGroup",
    "CanCreatePermissionGroup",
    "CanUpdatePermissionGroup",
    "CanDeletePermissionGroup",
]
