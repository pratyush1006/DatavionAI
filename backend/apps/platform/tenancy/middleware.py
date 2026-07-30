"""
Tenant resolution middleware.

Resolves tenant context for every request.

Provides:

- request.tenant
- request.tenant_membership
- request.tenant_context
- global tenant context


Resolution priority:

1. X-Tenant-ID header
2. UserTenantPreference
"""

from __future__ import annotations

from collections.abc import Callable

from django.http import (
    HttpRequest,
    HttpResponse,
)

from apps.platform.tenancy.context import (
    TenantContext,
    clear_current_tenant,
    set_tenant_context,
)
from apps.platform.tenancy.models import (
    UserTenantPreference,
)
from apps.platform.tenancy.selectors import (
    get_active_tenant,
    get_tenant_membership,
)


class TenantMiddleware:
    """
    Resolve active tenant.

    Flow:

    AuthenticationMiddleware
            |
            v
        request.user
            |
            +----------------+
            |                |
     X-Tenant-ID       UserTenantPreference
            |                |
            +----------------+
                     |
                     v
              Active Tenant
                     |
                     v
            TenantMembership
                     |
                     v
             TenantContext
    """

    def __init__(
        self,
        get_response: Callable[
            [HttpRequest],
            HttpResponse,
        ],
    ):
        self.get_response = get_response

    def __call__(
        self,
        request: HttpRequest,
    ) -> HttpResponse:

        request.tenant = None

        request.tenant_membership = None

        request.tenant_context = None

        user = getattr(
            request,
            "user",
            None,
        )

        if not user or not user.is_authenticated:
            return self.get_response(
                request,
            )

        tenant = None

        tenant_id = request.headers.get(
            "X-Tenant-ID",
        )

        if tenant_id:
            try:
                tenant = get_active_tenant(
                    tenant_id,
                )

            except (
                ValueError,
                TypeError,
            ):
                tenant = None

        if tenant is None:
            try:
                preference = (
                    UserTenantPreference.objects.select_related(
                        "tenant",
                    )
                    .filter(
                        user=user,
                    )
                    .first()
                )

                if preference:
                    tenant = get_active_tenant(
                        preference.tenant.id,
                    )

            except Exception:
                tenant = None

        if tenant is None:
            return self.get_response(
                request,
            )

        membership = get_tenant_membership(
            tenant_id=tenant.id,
            user_id=user.id,
        )

        if membership is None:
            return self.get_response(
                request,
            )

        context = TenantContext(
            tenant=tenant,
            user=user,
            membership=membership,
        )

        request.tenant = tenant

        request.tenant_membership = membership

        request.tenant_context = context

        set_tenant_context(
            context,
        )

        try:
            return self.get_response(
                request,
            )

        finally:
            clear_current_tenant()


__all__ = ("TenantMiddleware",)
