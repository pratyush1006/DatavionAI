"""
JWT authentication with DatavionOS tenant resolution.

Responsibilities:

- Authenticate JWT user
- Resolve active tenant
- Validate tenant membership
- Set tenant runtime context
- Attach tenant metadata to request
"""

from __future__ import annotations

from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)

from apps.platform.tenancy.context import (
    TenantContext,
    set_tenant_context,
)
from apps.platform.tenancy.selectors import (
    get_active_tenant,
    get_tenant_membership,
)


class TenantJWTAuthentication(
    JWTAuthentication,
):
    """
    JWT authentication with SaaS tenant resolution.
    """

    def authenticate(
        self,
        request,
    ):

        authenticated = super().authenticate(
            request,
        )

        if authenticated is None:
            return None

        user, token = authenticated

        tenant_id = request.headers.get(
            "X-Tenant-ID",
        )

        if tenant_id:
            tenant = get_active_tenant(
                tenant_id,
            )

            membership = get_tenant_membership(
                tenant_id=tenant.id,
                user_id=user.id,
            )

            if membership is not None:
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


__all__ = ("TenantJWTAuthentication",)
