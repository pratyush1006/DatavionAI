"""
Organization feature permissions.
"""

from __future__ import annotations

from apps.platform.rbac.permissions import (
    RBACPermissionBase,
)


class CanViewOrganizationFeature(
    RBACPermissionBase,
):
    """
    Permission to view organization features.
    """

    permission_code = "organizations.view"

    message = "You do not have permission to view organization features."


class CanCreateOrganizationFeature(
    RBACPermissionBase,
):
    """
    Permission to create organization features.
    """

    permission_code = "organizations.create"

    message = "You do not have permission to create organization features."


class CanUpdateOrganizationFeature(
    RBACPermissionBase,
):
    """
    Permission to update organization features.
    """

    permission_code = "organizations.update"

    message = "You do not have permission to update organization features."


class CanDeleteOrganizationFeature(
    RBACPermissionBase,
):
    """
    Permission to delete organization features.
    """

    permission_code = "organizations.delete"

    message = "You do not have permission to delete organization features."


__all__: tuple[str, ...] = (
    "CanViewOrganizationFeature",
    "CanCreateOrganizationFeature",
    "CanUpdateOrganizationFeature",
    "CanDeleteOrganizationFeature",
)
