"""Domain events emitted by Denials."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class DenialCreatedEvent(DomainEvent):
    """Signal creation of a denial."""

    denial_id: UUID
    organization_id: UUID
    patient_id: UUID


@dataclass(frozen=True)
class DenialStatusChangedEvent(DomainEvent):
    """Signal a denial status transition."""

    denial_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str


__all__ = ("DenialCreatedEvent", "DenialStatusChangedEvent")
