"""Domain events emitted by the Clinical Allergies bounded context."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class AllergyCreatedEvent(DomainEvent):
    allergy_id: UUID
    organization_id: UUID


@dataclass(frozen=True)
class AllergyUpdatedEvent(DomainEvent):
    allergy_id: UUID
    organization_id: UUID


@dataclass(frozen=True)
class AllergyDeletedEvent(DomainEvent):
    allergy_id: UUID
    organization_id: UUID


__all__ = (
    "AllergyCreatedEvent",
    "AllergyUpdatedEvent",
    "AllergyDeletedEvent",
)
