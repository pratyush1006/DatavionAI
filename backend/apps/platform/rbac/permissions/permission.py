"""
RBAC permission classes.

Uses DatavionOS RBAC authorization engine.

Responsibilities:

- Protect permission management APIs
- Delegate authorization to RBAC engine
- Enforce centralized RBAC permission codes
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)

# =============================================================================
# Permission API Permissions
# =============================================================================


class CanViewPermission(
    RBACPermissionBase,
):
    """
    Permission required to view permissions.
    """

    message = "You do not have permission to view permissions."

    permission_code = "rbac.view"


class CanCreatePermission(
    RBACPermissionBase,
):
    """
    Permission required to create permissions.
    """

    message = "You do not have permission to create permissions."

    permission_code = "rbac.create"


class CanUpdatePermission(
    RBACPermissionBase,
):
    """
    Permission required to update permissions.
    """

    message = "You do not have permission to update permissions."

    permission_code = "rbac.update"


class CanDeletePermission(
    RBACPermissionBase,
):
    """
    Permission required to delete permissions.
    """

    message = "You do not have permission to delete permissions."

    permission_code = "rbac.delete"


__all__ = [
    "CanViewPermission",
    "CanCreatePermission",
    "CanUpdatePermission",
    "CanDeletePermission",
]
