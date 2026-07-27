"""
Organization domain permissions.
"""

from __future__ import annotations

from apps.platform.rbac.permissions import (
    RBACPermissionBase,
)


class CanViewOrganizationDomain(
    RBACPermissionBase,
):
    """
    Permission to view organization domains.
    """

    permission_code = "organizations.view"

    message = "You do not have permission to view organization domains."


class CanCreateOrganizationDomain(
    RBACPermissionBase,
):
    """
    Permission to create organization domains.
    """

    permission_code = "organizations.create"

    message = "You do not have permission to create organization domains."


class CanUpdateOrganizationDomain(
    RBACPermissionBase,
):
    """
    Permission to update organization domains.
    """

    permission_code = "organizations.update"

    message = "You do not have permission to update organization domains."


class CanDeleteOrganizationDomain(
    RBACPermissionBase,
):
    """
    Permission to delete organization domains.
    """

    permission_code = "organizations.delete"

    message = "You do not have permission to delete organization domains."


__all__: tuple[str, ...] = (
    "CanViewOrganizationDomain",
    "CanCreateOrganizationDomain",
    "CanUpdateOrganizationDomain",
    "CanDeleteOrganizationDomain",
)
