"""
RBAC role hierarchy permission classes.

Uses DatavionOS RBAC authorization engine.

Responsibilities:

- Protect role hierarchy APIs
- Delegate authorization to RBAC engine
- Enforce centralized RBAC permission codes
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)

# =============================================================================
# Role Hierarchy API Permissions
# =============================================================================


class CanViewRoleHierarchy(
    RBACPermissionBase,
):
    """
    Permission required to view role hierarchies.
    """

    message = "You do not have permission to view role hierarchies."

    permission_code = "rbac.view"


class CanCreateRoleHierarchy(
    RBACPermissionBase,
):
    """
    Permission required to create role hierarchies.
    """

    message = "You do not have permission to create role hierarchies."

    permission_code = "rbac.create"


class CanUpdateRoleHierarchy(
    RBACPermissionBase,
):
    """
    Permission required to update role hierarchies.
    """

    message = "You do not have permission to update role hierarchies."

    permission_code = "rbac.update"


class CanDeleteRoleHierarchy(
    RBACPermissionBase,
):
    """
    Permission required to delete role hierarchies.
    """

    message = "You do not have permission to delete role hierarchies."

    permission_code = "rbac.delete"


__all__ = [
    "CanCreateRoleHierarchy",
    "CanDeleteRoleHierarchy",
    "CanUpdateRoleHierarchy",
    "CanViewRoleHierarchy",
]
