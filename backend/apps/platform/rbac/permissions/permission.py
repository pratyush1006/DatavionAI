"""
RBAC permission classes.
"""

from __future__ import annotations

from apps.common.permissions import (
    BasePermission,
)


class CanViewPermission(
    BasePermission,
):
    """
    Permission required to view permissions.
    """

    required_permission = "rbac.permission.view.organization"


class CanCreatePermission(
    BasePermission,
):
    """
    Permission required to create permissions.
    """

    required_permission = "rbac.permission.create.organization"


class CanUpdatePermission(
    BasePermission,
):
    """
    Permission required to update permissions.
    """

    required_permission = "rbac.permission.update.organization"


class CanDeletePermission(
    BasePermission,
):
    """
    Permission required to delete permissions.
    """

    required_permission = "rbac.permission.delete.organization"


__all__ = [
    "CanViewPermission",
    "CanCreatePermission",
    "CanUpdatePermission",
    "CanDeletePermission",
]
