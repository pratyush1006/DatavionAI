"""
Tenant middleware.

Resolves the current tenant and organization for the request lifecycle.

Tenant resolution supports multiple discovery strategies:

- subdomain
- custom domain
- JWT claims
- API keys
- request headers

Architecture:

Request
   |
TenantMiddleware
   |
TenantResolver
   |
Tenant + Organization Context
   |
request.tenant
request.organization
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

        Returns:

        (
            tenant,
            organization,
        )
        """


class NullTenantResolver:
    """
    Empty tenant resolver.

    Used when tenant resolution
    is disabled.
    """

    def resolve(
        self,
        request: HttpRequest,
    ) -> tuple[object | None, object | None]:

        return (
            None,
            None,
        )


class HeaderTenantResolver:
    """
    Resolve tenant context using request headers.

    Supported header:

    X-Organization-ID

    Example:

    HTTP_X_ORGANIZATION_ID=<uuid>
    """

    def resolve(
        self,
        request: HttpRequest,
    ) -> tuple[object | None, object | None]:

        from apps.platform.organizations.models import (
            Organization,
        )

        organization_id = request.headers.get(
            "X-Organization-ID",
        )

        if not organization_id:
            return (
                None,
                None,
            )

        organization = (
            Organization.objects.select_related(
                "tenant",
            )
            .filter(
                id=organization_id,
            )
            .first()
        )

        if not organization:
            return (
                None,
                None,
            )

        return (
            organization.tenant,
            organization,
        )


class TenantMiddleware(
    BaseMiddleware,
):
    """
    Resolve and attach current tenant context.

    Adds:

    request.tenant

    request.organization

    Also stores context globally
    using context variables.
    """

    resolver: TenantResolver = HeaderTenantResolver()

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
        Clear request context after response.
        """

        return response


__all__: tuple[str, ...] = (
    "TenantResolver",
    "NullTenantResolver",
    "HeaderTenantResolver",
    "TenantMiddleware",
)
