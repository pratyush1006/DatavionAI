"""Tenant-safe denial selectors."""

from __future__ import annotations

from django.db.models import QuerySet

from .models import Denial


def list_denials(*, organization_id, tenant_id) -> QuerySet[Denial]:
    """List active denials for an organization and tenant."""
    return Denial.objects.filter(
        organization_id=organization_id, organization__tenant_id=tenant_id
    )


def get_denial(*, organization_id, tenant_id, denial_id) -> Denial:
    """Get an active tenant-scoped denial."""
    return Denial.objects.get(
        id=denial_id, organization_id=organization_id, organization__tenant_id=tenant_id
    )


def get_denial_for_update(*, organization_id, tenant_id, denial_id) -> Denial:
    """Get a tenant-scoped denial with a row lock."""
    return Denial.objects.select_for_update().get(
        id=denial_id, organization_id=organization_id, organization__tenant_id=tenant_id
    )


def get_deleted_denial_for_update(*, organization_id, tenant_id, denial_id) -> Denial:
    """Get a deleted tenant-scoped denial with a row lock."""
    return Denial.all_objects.select_for_update().get(
        id=denial_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
        is_deleted=True,
    )


__all__ = (
    "list_denials",
    "get_denial",
    "get_denial_for_update",
    "get_deleted_denial_for_update",
)
