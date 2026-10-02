"""Resolve the active organization context for organization-scoped APIs."""

from __future__ import annotations

from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from apps.platform.organizations.models import Organization


class OrganizationContextMiddleware:
    """Attach a tenant-consistent organization selected by the client.

    This middleware only resolves context; it does not grant access. Each API
    still performs its own RBAC and object-scope checks. A supplied
    organization is ignored when it does not belong to the resolved tenant.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.organization = None
        # Older organization-scoped domains use these legacy request names.
        # Keep them aligned with the canonical context during their migration.
        request.current_organization = None

        organization_id = request.headers.get("X-Organization-ID")
        organization = (
            Organization.objects.select_related("tenant")
            .filter(pk=organization_id, is_active=True)
            .first()
            if organization_id
            else None
        )

        tenant = getattr(request, "tenant", None)
        if (
            organization is not None
            and tenant is not None
            and organization.tenant_id != tenant.id
        ):
            organization = None

        # First-party clients without an explicit active-organization header
        # retain their account's default organization, subject to the same
        # tenant consistency check.
        if organization is None:
            default_organization = getattr(
                getattr(request, "user", None), "organization", None
            )
            if (
                default_organization is not None
                and getattr(default_organization, "is_active", False)
                and (tenant is None or default_organization.tenant_id == tenant.id)
            ):
                organization = default_organization

        request.organization = organization
        # A selected organization is authoritative for the tenant of
        # organization-scoped requests. Tenant membership and RBAC continue
        # to be checked by the endpoint policy; this merely prevents legacy
        # domain APIs from receiving an incomplete request context.
        if organization is not None and getattr(request, "tenant", None) is None:
            request.tenant = organization.tenant
        request.current_tenant = getattr(request, "tenant", None)
        request.current_organization = organization
        return self.get_response(request)


__all__ = ("OrganizationContextMiddleware",)
