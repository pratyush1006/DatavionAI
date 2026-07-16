"""
RBAC role permission permission classes.
"""

from __future__ import annotations

from rest_framework.permissions import (
    BasePermission,
)


class CanViewRolePermission(
    BasePermission,
):
    """
    Permission to view role permissions.
    """

    message = "You do not have permission to view role permissions."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user may view role permissions.
        """

        return request.user.is_authenticated


class CanCreateRolePermission(
    BasePermission,
):
    """
    Permission to create role permissions.
    """

    message = "You do not have permission to assign role permissions."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user may create role permissions.
        """

        return request.user.is_authenticated


class CanUpdateRolePermission(
    BasePermission,
):
    """
    Permission to update role permissions.
    """

    message = "You do not have permission to update role permissions."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user may update role permissions.
        """

        return request.user.is_authenticated


class CanDeleteRolePermission(
    BasePermission,
):
    """
    Permission to delete role permissions.
    """

    message = "You do not have permission to delete role permissions."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user may delete role permissions.
        """

        return request.user.is_authenticated


__all__ = [
    "CanCreateRolePermission",
    "CanDeleteRolePermission",
    "CanUpdateRolePermission",
    "CanViewRolePermission",
]
