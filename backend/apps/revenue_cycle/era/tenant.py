"""Explicit tenant and organization context helpers for ERA APIs."""

from __future__ import annotations

from rest_framework.exceptions import NotFound


def resolve_context(request):
    """Require explicit tenant and organization context and validate their relationship."""

    try:
        tenant = request.tenant
        organization = request.organization
    except AttributeError as exc:
        raise NotFound("Explicit tenant and organization context is required.") from exc
    if tenant is None or organization is None:
        raise NotFound("Explicit tenant and organization context is required.")
    if organization.tenant_id != tenant.id:
        raise NotFound("Organization does not belong to the active tenant.")
    return tenant, organization


__all__ = ("resolve_context",)
