from __future__ import annotations

"""Explicit tenant and organization context helpers."""

from typing import Any

from rest_framework.exceptions import PermissionDenied


def require_context(request: Any) -> tuple[Any, Any]:
    """Require explicit request tenant and organization context."""

    tenant = getattr(request, "tenant", None)
    organization = getattr(request, "organization", None)

    if tenant is None or organization is None:
        raise PermissionDenied("Explicit tenant and organization context is required.")

    if getattr(organization, "tenant_id", None) != getattr(tenant, "id", None):
        raise PermissionDenied("Organization does not belong to the active tenant.")

    return tenant, organization


__all__ = ("require_context",)
