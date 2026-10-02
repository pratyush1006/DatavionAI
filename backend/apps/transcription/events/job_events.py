"""
Domain events for transcription-job lifecycle changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True, kw_only=True)
class TranscriptionCreatedEvent(DomainEvent):
    job_id: UUID
    organization_id: UUID
    patient_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class TranscriptionStartedEvent(DomainEvent):
    job_id: UUID
    organization_id: UUID
    patient_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class TranscriptionCompletedEvent(DomainEvent):
    job_id: UUID
    organization_id: UUID
    patient_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class TranscriptionFailedEvent(DomainEvent):
    job_id: UUID
    organization_id: UUID
    patient_id: UUID
    error_code: str
