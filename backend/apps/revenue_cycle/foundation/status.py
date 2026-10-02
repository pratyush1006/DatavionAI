"""Shared Revenue Cycle statuses."""

from __future__ import annotations

from enum import StrEnum


class RecordLifecycleStatus(StrEnum):
    """Generic lifecycle states."""

    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class ProcessingStatus(StrEnum):
    """Generic processing states."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


__all__ = (
    "ProcessingStatus",
    "RecordLifecycleStatus",
)
