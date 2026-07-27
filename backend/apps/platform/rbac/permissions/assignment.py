"""
RBAC role assignment permission classes.

Uses DatavionOS RBAC authorization engine.

Responsibilities:

- Protect role assignment operations
- Protect permission assignment operations
- Delegate authorization to RBAC engine
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)

# =============================================================================
# Role Assignment Permissions
# =============================================================================


class CanAssignRole(
    RBACPermissionBase,
):
    """
    Permission required to assign roles.
    """

    message = "You do not have permission to assign roles."

    permission_code = "rbac.assign"


class CanRemoveRole(
    RBACPermissionBase,
):
    """
    Permission required to remove roles.
    """

    message = "You do not have permission to remove roles."

    permission_code = "rbac.delete"


# =============================================================================
# Permission Assignment Permissions
# =============================================================================


class CanAssignPermission(
    RBACPermissionBase,
):
    """
    Permission required to assign permissions.
    """

    message = "You do not have permission to assign permissions."

    permission_code = "rbac.assign"


class CanRemovePermission(
    RBACPermissionBase,
):
    """
    Permission required to remove permissions.
    """

    message = "You do not have permission to remove permissions."

    permission_code = "rbac.delete"


__all__ = [
    "CanAssignPermission",
    "CanAssignRole",
    "CanRemovePermission",
    "CanRemoveRole",
]
