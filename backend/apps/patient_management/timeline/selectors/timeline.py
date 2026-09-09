"""
Read selectors for Patient Timeline.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.patient_management.timeline.models import TimelineEntry


def list_timeline(
    *,
    tenant_id: UUID,
    patient_id: UUID | None = None,
    organization_id: UUID | None = None,
) -> QuerySet[TimelineEntry]:
    """Return alive Timeline entries inside the tenant boundary."""

    queryset = TimelineEntry.objects.filter(
        organization__tenant_id=tenant_id,
    )

    if patient_id is not None:
        queryset = queryset.filter(
            patient_id=patient_id,
        )

    if organization_id is not None:
        queryset = queryset.filter(
            organization_id=organization_id,
        )

    return queryset.select_related(
        "organization",
        "patient",
        "created_by",
    )


def get_timeline(
    *,
    tenant_id: UUID,
    timeline_id: UUID,
    include_deleted: bool = False,
) -> TimelineEntry:
    """Return one Timeline entry within the tenant boundary."""

    manager = TimelineEntry.all_objects if include_deleted else TimelineEntry.objects

    return (
        manager.filter(
            pk=timeline_id,
            organization__tenant_id=tenant_id,
        )
        .select_related(
            "organization",
            "patient",
            "created_by",
        )
        .get()
    )


__all__ = (
    "get_timeline",
    "list_timeline",
)
