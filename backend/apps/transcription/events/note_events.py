"""
Domain events for generated-note lifecycle changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True, kw_only=True)
class ClinicalNoteGeneratedEvent(DomainEvent):
    note_id: UUID
    organization_id: UUID
    patient_id: UUID


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
