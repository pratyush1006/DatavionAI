"""
Organization branding permissions.
"""

from __future__ import annotations

from apps.platform.rbac.permissions import (
    RBACPermissionBase,
)


class CanViewOrganizationBranding(
    RBACPermissionBase,
):
    """
    Permission to view organization branding.
    """

    permission_code = "organizations.view"

    message = "You do not have permission to view organization branding."


class CanCreateOrganizationBranding(
    RBACPermissionBase,
):
    """
    Permission to create organization branding.
    """

    permission_code = "organizations.create"

    message = "You do not have permission to create organization branding."


class CanUpdateOrganizationBranding(
    RBACPermissionBase,
):
    """
    Permission to update organization branding.
    """

    permission_code = "organizations.update"

    message = "You do not have permission to update organization branding."


class CanDeleteOrganizationBranding(
    RBACPermissionBase,
):
    """
    Permission to delete organization branding.
    """

    permission_code = "organizations.delete"

    message = "You do not have permission to delete organization branding."


__all__: tuple[str, ...] = (
    "CanViewOrganizationBranding",
    "CanCreateOrganizationBranding",
    "CanUpdateOrganizationBranding",
    "CanDeleteOrganizationBranding",
)
