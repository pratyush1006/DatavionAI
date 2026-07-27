"""
Organization permissions.

Centralized RBAC permissions for Organization APIs.
"""

from __future__ import annotations

from apps.platform.rbac.permissions import (
    RBACPermissionBase,
)


class CanViewOrganization(
    RBACPermissionBase,
):
    """
    Permission to view organizations.
    """

    permission_code = "organizations.view"

    message = "You do not have permission to view organizations."


class CanCreateOrganization(
    RBACPermissionBase,
):
    """
    Permission to create organizations.
    """

    permission_code = "organizations.create"

    message = "You do not have permission to create organizations."


class CanUpdateOrganization(
    RBACPermissionBase,
):
    """
    Permission to update organizations.
    """

    permission_code = "organizations.update"

    message = "You do not have permission to update organizations."


class CanDeleteOrganization(
    RBACPermissionBase,
):
    """
    Permission to delete organizations.
    """

    permission_code = "organizations.delete"

    message = "You do not have permission to delete organizations."


__all__: tuple[str, ...] = (
    "CanViewOrganization",
    "CanCreateOrganization",
    "CanUpdateOrganization",
    "CanDeleteOrganization",
)
