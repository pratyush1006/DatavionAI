"""
RBAC role permission classes.

Uses DatavionOS RBAC authorization engine.

Responsibilities:

- Protect RBAC role permission APIs
- Delegate authorization to RBAC engine
- Enforce permission codes consistently
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)

# =============================================================================
# Role Permission API Permissions
# =============================================================================


class CanViewRolePermission(
    RBACPermissionBase,
):
    """
    Permission to view role permissions.
    """

    message = "You do not have permission to view role permissions."

    permission_code = "rbac.view"


class CanCreateRolePermission(
    RBACPermissionBase,
):
    """
    Permission to create role permissions.
    """

    message = "You do not have permission to create role permissions."

    permission_code = "rbac.create"


class CanUpdateRolePermission(
    RBACPermissionBase,
):
    """
    Permission to update role permissions.
    """

    message = "You do not have permission to update role permissions."

    permission_code = "rbac.update"


class CanDeleteRolePermission(
    RBACPermissionBase,
):
    """
    Permission to delete role permissions.
    """

    message = "You do not have permission to delete role permissions."

    permission_code = "rbac.delete"


__all__ = [
    "CanCreateRolePermission",
    "CanDeleteRolePermission",
    "CanUpdateRolePermission",
    "CanViewRolePermission",
]
