"""Explicit Revenue Cycle tenant isolation."""

from __future__ import annotations

from typing import Any

from apps.revenue_cycle.exceptions import RevenueCycleTenantContextError


def require_revenue_cycle_context(
    request: Any,
) -> tuple[Any, Any]:
    """Require explicit tenant and organization context."""
    tenant = getattr(request, "tenant", None)
    organization = getattr(request, "organization", None)

    if tenant is None:
        raise RevenueCycleTenantContextError(
            "Revenue Cycle requires explicit request.tenant context."
        )

    if organization is None:
        raise RevenueCycleTenantContextError(
            "Revenue Cycle requires explicit request.organization context."
        )

    tenant_id = getattr(tenant, "id", tenant)
    organization_tenant_id = getattr(
        organization,
        "tenant_id",
        None,
    )

    if organization_tenant_id is not None and organization_tenant_id != tenant_id:
        raise RevenueCycleTenantContextError(
            "Organization does not belong to the active tenant."
        )

    return tenant, organization


def ensure_organization_match(
    organization: Any,
    expected_organization: Any,
) -> None:
    """Ensure a resource belongs to the request organization."""
    organization_id = getattr(organization, "id", organization)
    expected_id = getattr(
        expected_organization,
        "id",
        expected_organization,
    )

    if organization_id != expected_id:
        raise RevenueCycleTenantContextError(
            "Resource organization does not match request organization."
        )


__all__ = (
    "ensure_organization_match",
    "require_revenue_cycle_context",
)
