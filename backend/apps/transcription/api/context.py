"""
Request tenant and organization boundary helpers.
"""

from __future__ import annotations

from rest_framework.exceptions import (
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)


def require_tenant_organization(request):
    if not request.user or not request.user.is_authenticated:
        raise NotAuthenticated()

    tenant = getattr(request, "tenant", None)
    organization = getattr(request, "organization", None)

    if tenant is None or organization is None:
        raise ValidationError("Active tenant and organization context are required.")

    tenant_id = getattr(tenant, "id", tenant)
    if getattr(organization, "tenant_id", None) != tenant_id:
        raise PermissionDenied("Organization does not belong to the active tenant.")

    return tenant, organization
