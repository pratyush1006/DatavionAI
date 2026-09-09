"""
Revenue Cycle Appeals selector exports.
"""

from __future__ import annotations

from uuid import UUID

from apps.revenue_cycle.appeals.models import Appeal


def list_appeals(*, organization_id: UUID, tenant_id: UUID):
    """Return active appeals in the explicit tenant scope."""
    return Appeal.objects.filter(
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
        is_deleted=False,
    ).select_related(
        "organization",
        "patient",
        "created_by",
        "updated_by",
    )


def get_appeal(
    *,
    organization_id: UUID,
    tenant_id: UUID,
    appeal_id: UUID,
):
    """Return one active tenant-scoped appeal."""
    return (
        list_appeals(
            organization_id=organization_id,
            tenant_id=tenant_id,
        )
        .filter(id=appeal_id)
        .first()
    )


def get_appeal_for_update(
    *,
    organization_id: UUID,
    tenant_id: UUID,
    appeal_id: UUID,
):
    """Return one active appeal with a row lock."""
    return (
        list_appeals(
            organization_id=organization_id,
            tenant_id=tenant_id,
        )
        .select_for_update()
        .filter(id=appeal_id)
        .first()
    )


def get_deleted_appeal_for_update(
    *,
    organization_id: UUID,
    tenant_id: UUID,
    appeal_id: UUID,
):
    """Return one deleted appeal with a row lock."""
    return (
        Appeal.all_objects.filter(
            id=appeal_id,
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
            is_deleted=True,
        )
        .select_for_update()
        .first()
    )


__all__ = (
    "get_appeal",
    "get_appeal_for_update",
    "get_deleted_appeal_for_update",
    "list_appeals",
)
