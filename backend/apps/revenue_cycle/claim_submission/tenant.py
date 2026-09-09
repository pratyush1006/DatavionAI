"""Explicit tenant and organization context resolution."""

from __future__ import annotations

from rest_framework.exceptions import PermissionDenied


def resolve_context(request):
    """Resolve and validate explicit tenant and organization context."""

    tenant = getattr(request, "tenant", None)
    organization = getattr(request, "organization", None)
    if tenant is None or organization is None:
        raise PermissionDenied("Explicit tenant and organization context is required.")
    if getattr(organization, "tenant_id", None) != getattr(tenant, "id", None):
        raise PermissionDenied("Organization does not belong to the active tenant.")
    return tenant, organization


__all__ = ("resolve_context",)
