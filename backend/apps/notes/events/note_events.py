"""Domain events for the Clinical Notes lifecycle."""

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True, kw_only=True)
class ClinicalNoteCreatedEvent(DomainEvent):
    note_id: UUID
    organization_id: UUID
    patient_id: UUID
    encounter_id: UUID | None


@dataclass(frozen=True, slots=True, kw_only=True)
class ClinicalNoteReviewedEvent(DomainEvent):
    note_id: UUID
    organization_id: UUID
    patient_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class ClinicalNoteSignedEvent(DomainEvent):
    note_id: UUID
    organization_id: UUID
    patient_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class ClinicalNoteAmendedEvent(DomainEvent):
    note_id: UUID
    organization_id: UUID
    patient_id: UUID
    amendment_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class ClinicalNoteCancelledEvent(DomainEvent):
    note_id: UUID
    organization_id: UUID
    patient_id: UUID
