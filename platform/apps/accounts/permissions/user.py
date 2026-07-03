"""
User permissions.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewUser(BasePermission):
    """
    Permission to view users.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.is_authenticated


class CanCreateUser(BasePermission):
    """
    Permission to create users.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.is_staff


class CanUpdateUser(BasePermission):
    """
    Permission to update users.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.is_staff


class CanDeleteUser(BasePermission):
    """
    Permission to delete users.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return request.user.is_superuser


__all__ = [
    "CanViewUser",
    "CanCreateUser",
    "CanUpdateUser",
    "CanDeleteUser",
]
