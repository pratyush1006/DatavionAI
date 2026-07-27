"""
Framework authentication permission classes.

Provides reusable authentication-related permissions for
DatavionOS.

These permissions are intentionally framework-only and must not
depend on RBAC, organizations, or feature modules.
"""

from __future__ import annotations

from rest_framework.permissions import (
    AllowAny as DRFAllowAny,
)
from rest_framework.permissions import (
    BasePermission,
)
from rest_framework.permissions import (
    IsAuthenticated as DRFIsAuthenticated,
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly as DRFIsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request
from rest_framework.views import APIView


class AllowAny(
    DRFAllowAny,
):
    """
    Allow unrestricted access.
    """


class IsAuthenticated(
    DRFIsAuthenticated,
):
    """
    Require an authenticated user.
    """


class IsAuthenticatedAndActive(
    DRFIsAuthenticated,
):
    """
    Require an authenticated and active user.
    """

    message = "Your account is inactive."

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        """
        Verify that the authenticated user is active.
        """

        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(
                request.user,
                "is_active",
                True,
            )
        )


class IsAuthenticatedOrReadOnly(
    DRFIsAuthenticatedOrReadOnly,
):
    """
    Allow read-only access for anonymous users and require
    authentication for write operations.
    """


class DenyAll(
    BasePermission,
):
    """
    Deny every request.
    """

    message = "Access is denied."

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        """
        Always deny access.
        """
        return False

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: object,
    ) -> bool:
        """
        Always deny object-level access.
        """
        return False


__all__ = (
    "AllowAny",
    "DenyAll",
    "IsAuthenticated",
    "IsAuthenticatedAndActive",
    "IsAuthenticatedOrReadOnly",
)
