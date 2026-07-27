"""
Organization hierarchy permissions.
"""

from __future__ import annotations

from apps.platform.rbac.permissions import (
    RBACPermissionBase,
)


class CanViewOrganizationHierarchy(
    RBACPermissionBase,
):
    """
    Permission to view organization hierarchies.
    """

    permission_code = "organizations.view"

    message = "You do not have permission to view organization hierarchies."


class CanCreateOrganizationHierarchy(
    RBACPermissionBase,
):
    """
    Permission to create organization hierarchies.
    """

    permission_code = "organizations.create"

    message = "You do not have permission to create organization hierarchies."


class CanUpdateOrganizationHierarchy(
    RBACPermissionBase,
):
    """
    Permission to update organization hierarchies.
    """

    permission_code = "organizations.update"

    message = "You do not have permission to update organization hierarchies."


class CanDeleteOrganizationHierarchy(
    RBACPermissionBase,
):
    """
    Permission to delete organization hierarchies.
    """

    permission_code = "organizations.delete"

    message = "You do not have permission to delete organization hierarchies."


__all__: tuple[str, ...] = (
    "CanViewOrganizationHierarchy",
    "CanCreateOrganizationHierarchy",
    "CanUpdateOrganizationHierarchy",
    "CanDeleteOrganizationHierarchy",
)
