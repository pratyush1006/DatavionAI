"""
RBAC PermissionGroup permission classes.

Uses DatavionOS RBAC authorization engine.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)

# =============================================================================
# Permission Group API Permissions
# =============================================================================


class CanViewPermissionGroup(
    RBACPermissionBase,
):
    """
    Permission required to view permission groups.
    """

    message = "You do not have permission to view permission groups."

    permission_code = "rbac.view"


class CanCreatePermissionGroup(
    RBACPermissionBase,
):
    """
    Permission required to create permission groups.
    """

    message = "You do not have permission to create permission groups."

    permission_code = "rbac.create"


class CanUpdatePermissionGroup(
    RBACPermissionBase,
):
    """
    Permission required to update permission groups.
    """

    message = "You do not have permission to update permission groups."

    permission_code = "rbac.update"


class CanDeletePermissionGroup(
    RBACPermissionBase,
):
    """
    Permission required to delete permission groups.
    """

    message = "You do not have permission to delete permission groups."

    permission_code = "rbac.delete"


__all__ = [
    "CanViewPermissionGroup",
    "CanCreatePermissionGroup",
    "CanUpdatePermissionGroup",
    "CanDeletePermissionGroup",
]
