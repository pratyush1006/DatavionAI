"""
User permissions.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class IsAuthenticatedUser(BasePermission):
    """
    Base permission requiring an authenticated user.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return bool(request.user and request.user.is_authenticated)


class CanViewUser(IsAuthenticatedUser):
    """
    Permission to view users.
    """


class CanCreateUser(IsAuthenticatedUser):
    """
    Permission to create users.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return super().has_permission(request, view) and request.user.is_staff


class CanUpdateUser(IsAuthenticatedUser):
    """
    Permission to update users.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return super().has_permission(request, view) and request.user.is_staff


class CanDeleteUser(IsAuthenticatedUser):
    """
    Permission to delete users.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return super().has_permission(request, view) and request.user.is_superuser


__all__ = [
    "CanCreateUser",
    "CanDeleteUser",
    "CanUpdateUser",
    "CanViewUser",
]
