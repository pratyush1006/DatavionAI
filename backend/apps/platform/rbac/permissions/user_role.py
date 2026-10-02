"""
RBAC user role permission classes.

Uses DatavionOS RBAC authorization engine.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)

# =============================================================================
# User Role API Permissions
# =============================================================================


class CanViewUserRole(
    RBACPermissionBase,
):
    """
    Permission to view user roles.
    """

    message = "You do not have permission to view user roles."

    permission_code = "rbac.view"


class CanCreateUserRole(
    RBACPermissionBase,
):
    """
    Permission to create user roles.
    """

    message = "You do not have permission to assign user roles."

    permission_code = "rbac.create"


class CanUpdateUserRole(
    RBACPermissionBase,
):
    """
    Permission to update user roles.
    """

    message = "You do not have permission to update user roles."

    permission_code = "rbac.update"


class CanDeleteUserRole(
    RBACPermissionBase,
):
    """
    Permission to delete user roles.
    """

    message = "You do not have permission to delete user roles."

    permission_code = "rbac.delete"


__all__ = [
    "CanCreateUserRole",
    "CanDeleteUserRole",
    "CanUpdateUserRole",
    "CanViewUserRole",
]
