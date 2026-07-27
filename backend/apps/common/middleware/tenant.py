"""
Tenant middleware.

Resolves the current tenant and organization for the request
lifecycle.

Tenant resolution is delegated to a resolver implementation so
DatavionAI can support multiple discovery strategies:

- subdomain
- custom domain
- JWT claims
- API keys
- request headers
"""

from __future__ import annotations

from typing import Protocol

from django.http import (
    HttpRequest,
    HttpResponseBase,
)

from apps.common.middleware.base import (
    BaseMiddleware,
)
from apps.common.middleware.context import (
    set_current_organization,
    set_current_tenant,
)


class TenantResolver(
    Protocol,
):
    """
    Contract for tenant resolution.
    """

    def resolve(
        self,
        request: HttpRequest,
    ) -> tuple[object | None, object | None]:
        """
        Resolve tenant and organization.
        """


class NullTenantResolver:
    """
    Default empty tenant resolver.
    """

    def resolve(
        self,
        request: HttpRequest,
    ) -> tuple[object | None, object | None]:
        """
        Return no tenant.
        """

        return (
            None,
            None,
        )


class TenantMiddleware(
    BaseMiddleware,
):
    """
    Resolve and attach current tenant context.
    """

    resolver: TenantResolver = NullTenantResolver()

    def process_request(
        self,
        request: HttpRequest,
    ) -> None:
        """
        Resolve tenant and organization.
        """

        tenant, organization = self.resolver.resolve(
            request,
        )

        if tenant is not None:
            request.tenant = tenant

            set_current_tenant(
                tenant,
            )

        if organization is not None:
            request.organization = organization

            set_current_organization(
                organization,
            )

    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponseBase,
    ) -> HttpResponseBase:
        """
        Return response unchanged.
        """

        return response


__all__: tuple[str, ...] = (
    "NullTenantResolver",
    "TenantMiddleware",
    "TenantResolver",
)
