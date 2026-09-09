"""Billing tenant and organization boundary helpers."""

from __future__ import annotations

from typing import Any

from apps.platform.organizations.models import Organization

from .exceptions import BillingPermissionError


def require_billing_tenant(request: Any) -> Any:
    """Require an explicit tenant context."""
    tenant = getattr(request, "tenant", None)
    if tenant is None:
        raise BillingPermissionError("Billing requires an explicit tenant context.")
    return tenant


def require_billing_organization(request: Any) -> Organization:
    """Require an explicit organization belonging to the active tenant."""
    tenant = require_billing_tenant(request)
    organization = getattr(request, "organization", None)
    if organization is None:
        raise BillingPermissionError(
            "Billing requires an explicit organization context."
        )
    if organization.tenant_id != tenant.id:
        raise BillingPermissionError(
            "Organization does not belong to the active tenant."
        )
    return organization


__all__ = ["require_billing_organization", "require_billing_tenant"]
