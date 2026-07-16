"""
Provider permissions.
"""

from __future__ import annotations

from rest_framework.permissions import BasePermission


class CanViewProvider(BasePermission):
    """
    Permission to view providers.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user can view providers.
        """

        return request.user.is_authenticated


class CanCreateProvider(BasePermission):
    """
    Permission to create providers.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user can create providers.
        """

        return request.user.is_authenticated


class CanUpdateProvider(BasePermission):
    """
    Permission to update providers.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user can update providers.
        """

        return request.user.is_authenticated


class CanDeleteProvider(BasePermission):
    """
    Permission to delete providers.
    """

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        """
        Return whether the user can delete providers.
        """

        return request.user.is_authenticated


__all__ = [
    "CanCreateProvider",
    "CanDeleteProvider",
    "CanUpdateProvider",
    "CanViewProvider",
]
