"""Patient Relationship restored event."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class PatientRelationshipRestoredEvent(DomainEvent):
    tenant_id: UUID
    actor_id: UUID
    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID


__all__ = ("PatientRelationshipRestoredEvent",)
