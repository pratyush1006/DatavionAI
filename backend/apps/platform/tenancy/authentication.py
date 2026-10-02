r"""
JWT authentication with DatavionOS tenant resolution.

Responsibilities
----------------

- Authenticate JWT users.
- Resolve the active tenant.
- Validate tenant membership.
- Establish the request tenant context.
- Attach tenant metadata to the DRF request.

Tenant resolution priority
--------------------------

1. X-Tenant-ID request header.
2. UserTenantPreference.

Security
--------

A tenant is never trusted solely because it exists.

The authenticated user must have an active TenantMembership for the
resolved tenant before TenantContext is established.

Invalid or unauthorized tenant selection fails closed.

Architecture
------------

    HTTP Request
         |
         v
    JWTAuthentication
         |
         v
    Authenticated User
         |
         v
    Tenant Resolution
      /           \
     /             \
X-Tenant-ID    UserTenantPreference
     \             /
      \           /
       v         v
       Active Tenant
            |
            v
    Active Membership
            |
            v
      TenantContext
            |
            v
    request.tenant
    request.tenant_membership
    request.tenant_context
"""

from __future__ import annotations

from typing import Any

from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)

from apps.platform.tenancy.context import (
    TenantContext,
    set_tenant_context,
)
from apps.platform.tenancy.models import (
    UserTenantPreference,
)
from apps.platform.tenancy.selectors import (
    get_active_tenant,
    get_tenant_membership,
)


class TenantJWTAuthentication(
    JWTAuthentication,
):
    """
    JWT authentication with DatavionOS tenant resolution.

    Tenant resolution happens after JWT authentication has successfully
    identified the user.

    The authenticated user is therefore the security principal used
    to validate tenant membership.

    Tenant resolution itself never grants access. Membership validation
    is mandatory before a TenantContext is established.
    """

    def authenticate(
        self,
        request: Any,
    ):
        """
        Authenticate the request and establish tenant context.

        Returns
        -------

        tuple
            ``(user, token)`` when JWT authentication succeeds.

        None
            When no authentication credentials are supplied.

        Notes
        -----

        Tenant resolution is intentionally performed after the parent
        JWT authentication succeeds.

        This prevents an unauthenticated request from influencing
        tenant context.
        """

        authenticated = super().authenticate(
            request,
        )

        if authenticated is None:
            return None

        user, token = authenticated

        tenant = self._resolve_tenant(
            request=request,
            user=user,
        )

        if tenant is None:
            return user, token

        membership = get_tenant_membership(
            tenant_id=tenant.id,
            user_id=user.id,
        )

        if membership is None:
            return user, token

        tenant_context = TenantContext(
            tenant=tenant,
            user=user,
            membership=membership,
        )

        set_tenant_context(
            tenant_context,
        )

        request.tenant = tenant
        request.tenant_membership = membership
        request.tenant_context = tenant_context

        return user, token

    # ==================================================================
    # Tenant Resolution
    # ==================================================================

    def _resolve_tenant(
        self,
        *,
        request: Any,
        user: Any,
    ):
        """
        Resolve the tenant requested by the authenticated user.

        Resolution priority:

        1. Explicit ``X-Tenant-ID`` header.
        2. Active ``UserTenantPreference``.

        An explicitly supplied tenant must not silently fall back to
        another tenant if that explicit tenant is invalid.

        Membership validation is performed by ``authenticate()`` after
        tenant resolution.
        """

        tenant_id = request.headers.get(
            "X-Tenant-ID",
        )

        if tenant_id:
            return self._resolve_header_tenant(
                tenant_id=tenant_id,
            )

        return self._resolve_preferred_tenant(
            user=user,
        )

    # ==================================================================
    # Header Tenant
    # ==================================================================

    @staticmethod
    def _resolve_header_tenant(
        *,
        tenant_id: str,
    ):
        """
        Resolve an explicitly requested active tenant.

        ``get_active_tenant()`` performs the database lookup and
        active-state filtering.

        Invalid UUID values are treated as an invalid tenant selection
        and fail closed.
        """

        try:
            return get_active_tenant(
                tenant_id,
            )

        except (
            ValueError,
            TypeError,
        ):
            return None

    # ==================================================================
    # Preferred Tenant
    # ==================================================================

    @staticmethod
    def _resolve_preferred_tenant(
        *,
        user: Any,
    ):
        """
        Resolve the user's preferred active tenant.

        ``UserTenantPreference`` is only a tenant-selection hint.

        It does not itself grant access.

        The resulting tenant is subsequently validated against an
        active ``TenantMembership``.
        """

        try:
            preference = (
                UserTenantPreference.objects.select_related(
                    "tenant",
                )
                .filter(
                    user=user,
                    is_active=True,
                    is_deleted=False,
                )
                .first()
            )

        except Exception:
            return None

        if preference is None:
            return None

        try:
            return get_active_tenant(
                preference.tenant_id,
            )

        except (
            ValueError,
            TypeError,
        ):
            return None


__all__ = ("TenantJWTAuthentication",)
