"""
Tenant membership selectors.

Read operations for tenant memberships.

Responsibilities:

- Fetch memberships
- Resolve user tenants
- Resolve tenant-user relationship
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.platform.tenancy.models import (
    TenantMembership,
)


def list_tenant_memberships(
    tenant_id: UUID,
) -> QuerySet[TenantMembership]:
    """
    Return active memberships for a tenant.
    """

    return TenantMembership.objects.filter(
        tenant_id=tenant_id,
        status=TenantMembership.Status.ACTIVE,
    ).select_related(
        "tenant",
        "user",
    )


def list_user_tenants(
    user_id: UUID,
) -> QuerySet[TenantMembership]:
    """
    Return active tenant memberships
    for a user.

    Used for:

    - Organization switcher
    - Tenant selection screen
    - Dashboard bootstrap
    """

    return (
        TenantMembership.objects.filter(
            user_id=user_id,
            status=TenantMembership.Status.ACTIVE,
        )
        .select_related(
            "tenant",
        )
        .order_by(
            "-is_owner",
            "-joined_at",
        )
    )


def get_tenant_membership(
    tenant_id: UUID,
    user_id: UUID,
) -> TenantMembership | None:
    """
    Return user membership in tenant.
    """

    return (
        TenantMembership.objects.filter(
            tenant_id=tenant_id,
            user_id=user_id,
            status=TenantMembership.Status.ACTIVE,
        )
        .select_related(
            "tenant",
            "user",
        )
        .first()
    )


__all__ = (
    "list_tenant_memberships",
    "list_user_tenants",
    "get_tenant_membership",
)
