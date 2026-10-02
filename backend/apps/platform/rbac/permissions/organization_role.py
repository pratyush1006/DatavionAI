"""
RBAC organization role permission classes.

Uses DatavionOS RBAC authorization engine.

Responsibilities:

- Protect organization role APIs
- Delegate authorization to RBAC engine
- Enforce RBAC permission codes consistently
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)

# =============================================================================
# Organization Role API Permissions
# =============================================================================


class CanViewOrganizationRole(
    RBACPermissionBase,
):
    """
    Permission required to view organization roles.
    """

    message = "You do not have permission to view organization roles."

    permission_code = "rbac.view"


class CanCreateOrganizationRole(
    RBACPermissionBase,
):
    """
    Permission required to create organization roles.
    """

    message = "You do not have permission to create organization roles."

    permission_code = "rbac.create"


class CanUpdateOrganizationRole(
    RBACPermissionBase,
):
    """
    Permission required to update organization roles.
    """

    message = "You do not have permission to update organization roles."

    permission_code = "rbac.update"


class CanDeleteOrganizationRole(
    RBACPermissionBase,
):
    """
    Permission required to delete organization roles.
    """

    message = "You do not have permission to delete organization roles."

    permission_code = "rbac.delete"


__all__ = [
    "CanCreateOrganizationRole",
    "CanDeleteOrganizationRole",
    "CanUpdateOrganizationRole",
    "CanViewOrganizationRole",
]
