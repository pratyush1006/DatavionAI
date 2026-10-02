from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class DiagnosisCreated(DomainEvent):
    diagnosis_id: UUID
    organization_id: UUID
    encounter_id: UUID
    diagnosis_code: str
    status: str


@dataclass(frozen=True, slots=True)
class DiagnosisUpdated(DomainEvent):
    diagnosis_id: UUID
    organization_id: UUID


@dataclass(frozen=True, slots=True)
class DiagnosisDeleted(DomainEvent):
    diagnosis_id: UUID
    organization_id: UUID
