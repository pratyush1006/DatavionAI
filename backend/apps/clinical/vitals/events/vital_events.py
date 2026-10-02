from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class VitalCreatedEvent(DomainEvent):
    vital_id: UUID
    organization_id: UUID


@dataclass(frozen=True)
class VitalUpdatedEvent(DomainEvent):
    vital_id: UUID
    organization_id: UUID


@dataclass(frozen=True)
class VitalDeletedEvent(DomainEvent):
    vital_id: UUID
    organization_id: UUID


__all__ = ("VitalCreatedEvent", "VitalUpdatedEvent", "VitalDeletedEvent")
