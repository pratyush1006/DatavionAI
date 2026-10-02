"""
Role API permissions.

Uses DatavionOS RBAC authorization engine.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)

# =============================================================================
# Role API Permissions
# =============================================================================


class CanViewRole(
    RBACPermissionBase,
):
    """
    Permission required to view roles.
    """

    message = "You do not have permission to view roles."

    permission_code = "rbac.view"


class CanCreateRole(
    RBACPermissionBase,
):
    """
    Permission required to create roles.
    """

    message = "You do not have permission to create roles."

    permission_code = "rbac.create"


class CanUpdateRole(
    RBACPermissionBase,
):
    """
    Permission required to update roles.
    """

    message = "You do not have permission to update roles."

    permission_code = "rbac.update"


class CanDeleteRole(
    RBACPermissionBase,
):
    """
    Permission required to delete roles.
    """

    message = "You do not have permission to delete roles."

    permission_code = "rbac.delete"


__all__ = [
    "CanCreateRole",
    "CanDeleteRole",
    "CanUpdateRole",
    "CanViewRole",
]
