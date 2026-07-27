"""
Shared status enumerations for the DatavionOS platform.

Defines common lifecycle and operational states used
across platform modules.
"""

from __future__ import annotations

from enum import StrEnum


class HealthStatus(StrEnum):
    """
    Platform health status.
    """

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNHEALTHY = "unhealthy"


class ResourceStatus(StrEnum):
    """
    Generic resource lifecycle status.

    Used by reusable business entities.
    """

    DRAFT = "draft"

    PENDING = "pending"

    ACTIVE = "active"

    INACTIVE = "inactive"

    DISABLED = "disabled"

    SUSPENDED = "suspended"

    ARCHIVED = "archived"

    EXPIRED = "expired"

    FAILED = "failed"

    DELETED = "deleted"


class OperationStatus(StrEnum):
    """
    Long-running operation status.

    Used by:
    - AI processing
    - imports
    - exports
    - background jobs
    - workflows
    """

    QUEUED = "queued"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


__all__ = [
    "HealthStatus",
    "OperationStatus",
    "ResourceStatus",
]
