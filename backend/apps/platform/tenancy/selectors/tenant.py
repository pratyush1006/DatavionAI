"""
Tenant selectors.

Read-only database access layer
for tenant operations.
"""

from __future__ import annotations

from uuid import UUID

from apps.platform.tenancy.models import (
    Tenant,
)


def get_tenant(
    tenant_id: UUID,
) -> Tenant | None:
    """
    Retrieve tenant by UUID.
    """

    return Tenant.objects.filter(
        id=tenant_id,
    ).first()


def get_tenant_by_slug(
    slug: str,
) -> Tenant | None:
    """
    Retrieve tenant by slug.
    """

    return Tenant.objects.by_slug(
        slug,
    ).first()


def get_active_tenant(
    tenant_id: UUID,
) -> Tenant | None:
    """
    Retrieve active tenant.
    """

    return (
        Tenant.objects.active()
        .filter(
            id=tenant_id,
        )
        .first()
    )


def list_active_tenants():
    """
    Return all active tenants.
    """

    return Tenant.objects.active()


__all__ = (
    "get_tenant",
    "get_tenant_by_slug",
    "get_active_tenant",
    "list_active_tenants",
)
