"""
Domain services for Patient Timeline.

Services perform domain mutations and do not authorize HTTP requests.
"""

from __future__ import annotations

from typing import Any

from apps.patient_management.timeline.constants import TimelineStatus
from apps.patient_management.timeline.models import TimelineEntry


def create_timeline(
    *,
    validated_data: dict[str, Any],
    performed_by,
) -> TimelineEntry:
    """Create a Timeline entry from validated workflow data."""

    instance = TimelineEntry(
        **validated_data,
        created_by=performed_by,
        status=validated_data.get(
            "status",
            TimelineStatus.ACTIVE,
        ),
    )

    if instance.status == TimelineStatus.ACTIVE:
        instance.is_active = True
    else:
        instance.is_active = False

    instance.save()
    return instance


def update_timeline(
    *,
    instance: TimelineEntry,
    validated_data: dict[str, Any],
) -> TimelineEntry:
    """Update mutable Timeline fields."""

    mutable_fields = {
        "event_type",
        "title",
        "description",
        "occurred_at",
        "metadata",
    }

    for field_name, value in validated_data.items():
        if field_name in mutable_fields:
            setattr(
                instance,
                field_name,
                value,
            )

    instance.save()
    return instance


def activate_timeline(
    *,
    instance: TimelineEntry,
    performed_by=None,
) -> TimelineEntry:
    """Activate an alive Timeline entry without restoring deleted data."""

    if instance.is_deleted:
        raise ValueError(
            "A deleted Timeline entry must be restored before activation.",
        )

    instance.status = TimelineStatus.ACTIVE
    instance.is_active = True
    instance.save(
        update_fields=(
            "status",
            "is_active",
            "updated_at",
        ),
    )
    return instance


def deactivate_timeline(
    *,
    instance: TimelineEntry,
    performed_by=None,
) -> TimelineEntry:
    """Move an alive Timeline entry into the draft state."""

    if instance.is_deleted:
        raise ValueError(
            "A deleted Timeline entry cannot be deactivated.",
        )

    instance.status = TimelineStatus.DRAFT
    instance.is_active = False
    instance.save(
        update_fields=(
            "status",
            "is_active",
            "updated_at",
        ),
    )
    return instance


def archive_timeline(
    *,
    instance: TimelineEntry,
    performed_by=None,
) -> TimelineEntry:
    """Archive an alive Timeline entry without soft-deleting it."""

    if instance.is_deleted:
        raise ValueError(
            "A deleted Timeline entry cannot be archived.",
        )

    instance.status = TimelineStatus.ARCHIVED
    instance.is_active = False
    instance.save(
        update_fields=(
            "status",
            "is_active",
            "updated_at",
        ),
    )
    return instance


def delete_timeline(
    *,
    instance: TimelineEntry,
    performed_by=None,
) -> None:
    """Soft-delete a Timeline entry through the platform lifecycle."""

    if instance.is_deleted:
        return

    instance.status = TimelineStatus.ARCHIVED
    instance.is_active = False
    instance.save(
        update_fields=(
            "status",
            "is_active",
            "updated_at",
        ),
    )

    user_id = getattr(
        performed_by,
        "id",
        None,
    )
    instance.delete(
        user_id=user_id,
    )


def restore_timeline(
    *,
    instance: TimelineEntry,
    performed_by=None,
) -> TimelineEntry:
    """Restore a deleted Timeline entry into a safe draft state."""

    if not instance.is_deleted:
        return instance

    instance.restore()
    instance.status = TimelineStatus.DRAFT
    instance.is_active = False
    instance.save(
        update_fields=(
            "status",
            "is_active",
            "updated_at",
        ),
    )
    return instance


__all__ = (
    "activate_timeline",
    "archive_timeline",
    "create_timeline",
    "deactivate_timeline",
    "delete_timeline",
    "restore_timeline",
    "update_timeline",
)
