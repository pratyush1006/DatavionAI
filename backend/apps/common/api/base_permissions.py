"""
Reusable DRF permission classes.

These permission classes provide generic authorization helpers
that can be shared across all feature applications.

Business-specific permissions (RBAC) belong in
apps.platform.rbac.permissions.
"""

from __future__ import annotations

from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthenticatedAndActive(BasePermission):
    """
    Allow access only to authenticated active users.
    """

    message = "Authentication is required or the user account is inactive."

    def has_permission(
        self,
        request: Request,
        _view: APIView,
    ) -> bool:
        """
        Determine whether the current user is authenticated and active.
        """

        user = request.user

        return bool(
            user and user.is_authenticated and getattr(user, "is_active", False)
        )


class AllowAnyAuthenticated(BasePermission):
    """
    Allow access to any authenticated user.
    """

    message = "Authentication is required."

    def has_permission(
        self,
        request: Request,
        _view: APIView,
    ) -> bool:
        """
        Determine whether the current user is authenticated.
        """

        user = request.user

        return bool(user and user.is_authenticated)


class ReadOnly(BasePermission):
    """
    Allow read-only HTTP methods.
    """

    def has_permission(
        self,
        request: Request,
        _view: APIView,
    ) -> bool:
        """
        Determine whether the request uses a safe HTTP method.
        """

        return request.method in SAFE_METHODS


class DenyAll(BasePermission):
    """
    Deny every request.
    """

    message = "Access denied."

    def has_permission(
        self,
        request: Request,
        _view: APIView,
    ) -> bool:
        """
        Always deny access.
        """

        return False


__all__ = [
    "AllowAnyAuthenticated",
    "DenyAll",
    "IsAuthenticatedAndActive",
    "ReadOnly",
]
