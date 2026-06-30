"""
Reusable DRF permission classes.

These permission classes provide generic authorization helpers
that can be shared across all feature applications.

Business-specific permissions (RBAC) belong in
apps.rbac.permissions.
"""

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

    message = "Authentication is required."

    def has_permission(
        self,
        request: Request,
        _view: APIView,
    ) -> bool:
        user = request.user

        return bool(user and user.is_authenticated and user.is_active)


class ReadOnly(BasePermission):
    """
    Allow read-only requests.
    """

    def has_permission(
        self,
        request: Request,
        _view: APIView,
    ) -> bool:
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
        return False


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
        return bool(request.user and request.user.is_authenticated)


__all__ = [
    "AllowAnyAuthenticated",
    "DenyAll",
    "IsAuthenticatedAndActive",
    "ReadOnly",
]
