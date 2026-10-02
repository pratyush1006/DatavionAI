from __future__ import annotations

"""Tenant-safe Coding selectors."""

from uuid import UUID

from django.db.models import QuerySet

from ..models import CodingRecord


def _tenant_filter(queryset: QuerySet, tenant_id: UUID | None) -> QuerySet:
    """Apply an optional tenant boundary to a Coding queryset."""

    if tenant_id is None:
        return queryset

    return queryset.filter(
        organization__tenant_id=tenant_id,
    )


def list_coding_records(
    *,
    organization_id: UUID,
    tenant_id: UUID,
) -> QuerySet[CodingRecord]:
    """List active Coding records inside explicit tenant boundaries."""

    queryset = CodingRecord.objects.filter(
        organization_id=organization_id,
    )
    queryset = _tenant_filter(queryset, tenant_id)

    return queryset.select_related(
        "patient",
        "organization",
        "assigned_to",
        "reviewed_by",
        "validated_by",
        "released_by",
    ).prefetch_related("code_assignments")


def get_coding_record(
    *,
    organization_id: UUID,
    record_id: UUID,
    tenant_id: UUID,
) -> CodingRecord:
    """Retrieve one active Coding record inside tenant boundaries."""

    queryset = CodingRecord.objects.filter(
        organization_id=organization_id,
        id=record_id,
    )
    queryset = _tenant_filter(queryset, tenant_id)

    return (
        queryset.select_related(
            "patient",
            "organization",
            "assigned_to",
            "reviewed_by",
            "validated_by",
            "released_by",
        )
        .prefetch_related("code_assignments")
        .get()
    )


def get_coding_record_for_update(
    *,
    organization_id: UUID,
    record_id: UUID,
    tenant_id: UUID,
) -> CodingRecord:
    """Retrieve an active Coding record with a row lock."""

    queryset = CodingRecord.objects.select_for_update().filter(
        organization_id=organization_id,
        id=record_id,
    )
    queryset = _tenant_filter(queryset, tenant_id)
    return queryset.get()


def get_deleted_coding_record_for_update(
    *,
    organization_id: UUID,
    record_id: UUID,
    tenant_id: UUID,
) -> CodingRecord:
    """Retrieve a deleted Coding record with a row lock."""

    queryset = CodingRecord.all_objects.select_for_update().filter(
        organization_id=organization_id,
        id=record_id,
        is_deleted=True,
    )
    queryset = _tenant_filter(queryset, tenant_id)
    return queryset.get()


__all__ = (
    "get_coding_record",
    "get_coding_record_for_update",
    "get_deleted_coding_record_for_update",
    "list_coding_records",
)
