"""Explicit tenant and organization resolution."""

from __future__ import annotations

from rest_framework.exceptions import PermissionDenied


def resolve_context(request):
    """Return explicit request tenant and organization context."""

    tenant = getattr(request, "tenant", None)
    organization = getattr(request, "organization", None)
    if tenant is None or organization is None:
        raise PermissionDenied("Explicit tenant and organization context is required.")
    if str(getattr(organization, "tenant_id", "")) != str(tenant.id):
        raise PermissionDenied("Organization does not belong to the request tenant.")
    return tenant, organization


__all__ = ("resolve_context",)
