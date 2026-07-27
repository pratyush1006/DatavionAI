"""
Reusable DRF permission classes.

Framework-level authorization helpers for DatavionOS.

Business authorization rules belong to feature applications:

- RBAC
- Ownership
- Subscription rules
- Feature access
- Clinical permissions
"""

from __future__ import annotations

from typing import Any, Final

from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)
from rest_framework.request import Request
from rest_framework.views import APIView

AUTHENTICATION_REQUIRED_MESSAGE: Final[str] = "Authentication is required."

ACCOUNT_INACTIVE_MESSAGE: Final[str] = "The authenticated account is inactive."

TENANT_INACTIVE_MESSAGE: Final[str] = "Tenant access is unavailable."

ACCESS_DENIED_MESSAGE: Final[str] = "Access denied."


class DatavionPermission(
    BasePermission,
):
    """
    Base permission for DatavionOS.

    All reusable framework permissions should
    inherit from this class.
    """

    @staticmethod
    def get_user(
        request: Request,
    ) -> Any:
        """
        Return request user.
        """

        return request.user

    @staticmethod
    def get_tenant(
        request: Request,
    ) -> Any:
        """
        Return current tenant.

        Provided by tenant middleware.
        """

        return getattr(
            request,
            "tenant",
            None,
        )

    @classmethod
    def is_authenticated(
        cls,
        request: Request,
    ) -> bool:
        """
        Check authentication.
        """

        user = cls.get_user(request)

        return bool(
            user
            and getattr(
                user,
                "is_authenticated",
                False,
            )
        )

    @classmethod
    def is_active(
        cls,
        request: Request,
    ) -> bool:
        """
        Check user active status.
        """

        user = cls.get_user(request)

        return bool(
            user
            and getattr(
                user,
                "is_active",
                False,
            )
        )

    @classmethod
    def has_tenant_access(
        cls,
        request: Request,
    ) -> bool:
        """
        Validate tenant availability.
        """

        tenant = cls.get_tenant(
            request,
        )

        # Allow non-tenant infrastructure APIs
        if tenant is None:
            return True

        return getattr(
            tenant,
            "is_active",
            True,
        )

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: object,
    ) -> bool:
        """
        Default object permission behavior.
        """

        return self.has_permission(
            request,
            view,
        )


class AllowAnyAuthenticated(
    DatavionPermission,
):
    """
    Allow authenticated users.
    """

    message = AUTHENTICATION_REQUIRED_MESSAGE

    def has_permission(
        self,
        request: Request,
        _view: APIView,
    ) -> bool:

        return self.is_authenticated(
            request,
        )


class IsAuthenticatedAndActive(
    DatavionPermission,
):
    """
    Allow authenticated active users
    with active tenant access.
    """

    message = ACCOUNT_INACTIVE_MESSAGE

    def has_permission(
        self,
        request: Request,
        _view: APIView,
    ) -> bool:

        return (
            self.is_authenticated(request)
            and self.is_active(request)
            and self.has_tenant_access(request)
        )


class ReadOnly(
    DatavionPermission,
):
    """
    Allow only safe methods.
    """

    def has_permission(
        self,
        request: Request,
        _view: APIView,
    ) -> bool:

        return request.method in SAFE_METHODS


class DenyAll(
    DatavionPermission,
):
    """
    Deny every request.
    """

    message = ACCESS_DENIED_MESSAGE

    def has_permission(
        self,
        request: Request,
        _view: APIView,
    ) -> bool:

        return False


__all__: tuple[str, ...] = (
    "AllowAnyAuthenticated",
    "DatavionPermission",
    "DenyAll",
    "IsAuthenticatedAndActive",
    "ReadOnly",
)
