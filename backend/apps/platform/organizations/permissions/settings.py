"""
Organization settings permissions.
"""

from __future__ import annotations

from apps.platform.rbac.permissions import (
    RBACPermissionBase,
)


class CanViewOrganizationSettings(
    RBACPermissionBase,
):
    """
    Permission to view organization settings.
    """

    permission_code = "organizations.view"

    message = "You do not have permission to view organization settings."


class CanCreateOrganizationSettings(
    RBACPermissionBase,
):
    """
    Permission to create organization settings.
    """

    permission_code = "organizations.create"

    message = "You do not have permission to create organization settings."


class CanUpdateOrganizationSettings(
    RBACPermissionBase,
):
    """
    Permission to update organization settings.
    """

    permission_code = "organizations.update"

    message = "You do not have permission to update organization settings."


class CanDeleteOrganizationSettings(
    RBACPermissionBase,
):
    """
    Permission to delete organization settings.
    """

    permission_code = "organizations.delete"

    message = "You do not have permission to delete organization settings."


__all__: tuple[str, ...] = (
    "CanViewOrganizationSettings",
    "CanCreateOrganizationSettings",
    "CanUpdateOrganizationSettings",
    "CanDeleteOrganizationSettings",
)
