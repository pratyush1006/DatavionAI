"""
Organization permission classes.
"""

from __future__ import annotations

from typing import Final

from apps.common.permissions import DatavionPermission


class CanViewOrganization(DatavionPermission):
    """
    Permission required to view organizations.
    """

    permission_code: Final[str] = "organization.view"


class CanCreateOrganization(DatavionPermission):
    """
    Permission required to create organizations.
    """

    permission_code: Final[str] = "organization.create"


class CanUpdateOrganization(DatavionPermission):
    """
    Permission required to update organizations.
    """

    permission_code: Final[str] = "organization.update"


class CanDeleteOrganization(DatavionPermission):
    """
    Permission required to delete organizations.
    """

    permission_code: Final[str] = "organization.delete"


__all__ = [
    "CanCreateOrganization",
    "CanDeleteOrganization",
    "CanUpdateOrganization",
    "CanViewOrganization",
]
