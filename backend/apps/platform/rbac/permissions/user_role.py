"""
RBAC user role permission classes.
"""

from __future__ import annotations

from rest_framework.permissions import (
    BasePermission,
)


class CanViewUserRole(
    BasePermission,
):
    """
    Permission to view user roles.
    """

    message = "You do not have permission to view user roles."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user may view user roles.
        """

        return request.user.is_authenticated


class CanCreateUserRole(
    BasePermission,
):
    """
    Permission to create user roles.
    """

    message = "You do not have permission to assign user roles."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user may create user roles.
        """

        return request.user.is_authenticated


class CanUpdateUserRole(
    BasePermission,
):
    """
    Permission to update user roles.
    """

    message = "You do not have permission to update user roles."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user may update user roles.
        """

        return request.user.is_authenticated


class CanDeleteUserRole(
    BasePermission,
):
    """
    Permission to delete user roles.
    """

    message = "You do not have permission to delete user roles."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user may delete user roles.
        """

        return request.user.is_authenticated


__all__ = [
    "CanCreateUserRole",
    "CanDeleteUserRole",
    "CanUpdateUserRole",
    "CanViewUserRole",
]
