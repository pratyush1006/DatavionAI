"""Tenant-safe ERA selectors."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from .models import ERA


def eras_for_organization(*, organization_id: UUID, tenant_id: UUID) -> QuerySet[ERA]:
    """Return active ERAs within explicit tenant and organization scope."""

    return ERA.objects.filter(
        organization_id=organization_id, organization__tenant_id=tenant_id
    )


def get_era(*, organization_id: UUID, tenant_id: UUID, era_id: UUID) -> ERA:
    """Return an active ERA in tenant scope."""

    return eras_for_organization(
        organization_id=organization_id, tenant_id=tenant_id
    ).get(pk=era_id)


def get_era_for_update(*, organization_id: UUID, tenant_id: UUID, era_id: UUID) -> ERA:
    """Return an active ERA with a database row lock."""

    return (
        eras_for_organization(organization_id=organization_id, tenant_id=tenant_id)
        .select_for_update()
        .get(pk=era_id)
    )


def get_deleted_era_for_update(
    *, organization_id: UUID, tenant_id: UUID, era_id: UUID
) -> ERA:
    """Return a deleted ERA with a database row lock."""

    return (
        ERA.all_objects.filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
            pk=era_id,
            is_deleted=True,
        )
        .select_for_update()
        .get()
    )


__all__ = (
    "eras_for_organization",
    "get_deleted_era_for_update",
    "get_era",
    "get_era_for_update",
)
