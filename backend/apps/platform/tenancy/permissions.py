"""
Tenant permissions for DatavionOS.

Provides tenant-level access control.

Supports:

- Platform administration
- Tenant access validation
- Tenant context enforcement
- Tenant ownership checks

Future integration:

RBAC
 |
 TenantRole
 |
 Permission
"""

from __future__ import annotations

from rest_framework.permissions import (
    BasePermission,
)

from apps.platform.tenancy.context import (
    get_tenant_context,
)


class IsPlatformAdmin(
    BasePermission,
):
    """
    Platform administrators can manage
    all tenants.
    """

    message = "Platform administrator permission required."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        user = getattr(
            request,
            "user",
            None,
        )

        return bool(
            user
            and user.is_authenticated
            and getattr(
                user,
                "is_staff",
                False,
            )
        )


class HasTenantAccess(
    BasePermission,
):
    """
    Verify user has access to current tenant.

    Used by tenant-scoped APIs.
    """

    message = "You do not have access to this tenant."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        tenant = getattr(
            request,
            "tenant",
            None,
        )

        user = getattr(
            request,
            "user",
            None,
        )

        if not user or not user.is_authenticated:
            return False

        if not tenant:
            return False

        membership = getattr(
            request,
            "tenant_membership",
            None,
        )

        return membership is not None


class IsTenantAdmin(
    BasePermission,
):
    """
    Tenant administrator permission.

    Future:
    RBAC Tenant Admin role.
    """

    message = "Tenant administrator permission required."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        user = getattr(
            request,
            "user",
            None,
        )

        if not user or not user.is_authenticated:
            return False

        return bool(
            getattr(
                user,
                "is_staff",
                False,
            )
        )


class TenantRequiredPermission(
    BasePermission,
):
    """
    Require active tenant context.

    Used by tenant-isolated APIs.
    """

    message = "Active tenant context is required."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        return get_tenant_context() is not None


class TenantOwnerPermission(
    BasePermission,
):
    """
    Require tenant owner access.
    """

    message = "Tenant owner permission required."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        context = get_tenant_context()

        if context is None:
            return False

        return bool(context.membership.is_owner)


__all__ = (
    "IsPlatformAdmin",
    "HasTenantAccess",
    "IsTenantAdmin",
    "TenantRequiredPermission",
    "TenantOwnerPermission",
)
