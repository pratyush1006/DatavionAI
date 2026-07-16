"""
Organization role permissions.
"""

from __future__ import annotations

from apps.common.permissions import DatavionPermission


class CanViewOrganizationRole(DatavionPermission):
    """
    Permission required to view organization roles.
    """

    permission_code = "organization_role.view"


class CanCreateOrganizationRole(DatavionPermission):
    """
    Permission required to create organization roles.
    """

    permission_code = "organization_role.create"


class CanUpdateOrganizationRole(DatavionPermission):
    """
    Permission required to update organization roles.
    """

    permission_code = "organization_role.update"


class CanDeleteOrganizationRole(DatavionPermission):
    """
    Permission required to delete organization roles.
    """

    permission_code = "organization_role.delete"


__all__ = [
    "CanCreateOrganizationRole",
    "CanDeleteOrganizationRole",
    "CanUpdateOrganizationRole",
    "CanViewOrganizationRole",
]
