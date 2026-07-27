"""
Organization module permissions.
"""

from __future__ import annotations

from apps.platform.rbac.permissions import (
    RBACPermissionBase,
)


class CanViewOrganizationModule(
    RBACPermissionBase,
):
    """
    Permission to view organization modules.
    """

    permission_code = "organizations.view"

    message = "You do not have permission to view organization modules."


class CanCreateOrganizationModule(
    RBACPermissionBase,
):
    """
    Permission to create organization modules.
    """

    permission_code = "organizations.create"

    message = "You do not have permission to create organization modules."


class CanUpdateOrganizationModule(
    RBACPermissionBase,
):
    """
    Permission to update organization modules.
    """

    permission_code = "organizations.update"

    message = "You do not have permission to update organization modules."


class CanDeleteOrganizationModule(
    RBACPermissionBase,
):
    """
    Permission to delete organization modules.
    """

    permission_code = "organizations.delete"

    message = "You do not have permission to delete organization modules."


__all__: tuple[str, ...] = (
    "CanViewOrganizationModule",
    "CanCreateOrganizationModule",
    "CanUpdateOrganizationModule",
    "CanDeleteOrganizationModule",
)
