"""
Patient Timeline restored domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
)
class TimelineRestoredEvent(DomainEvent):
    """Represent committed restoration of a deleted Timeline entry."""

    tenant_id: UUID
    actor_id: UUID
    timeline_id: UUID
    patient_id: UUID
    organization_id: UUID


__all__ = ("TimelineRestoredEvent",)
