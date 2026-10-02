from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class EncounterCreated(DomainEvent):
    encounter_id: UUID
    organization_id: UUID
    patient_id: UUID
    provider_id: UUID
    appointment_id: UUID
    status: str


@dataclass(frozen=True, slots=True)
class EncounterUpdated(DomainEvent):
    encounter_id: UUID
    organization_id: UUID


@dataclass(frozen=True, slots=True)
class EncounterStatusChanged(DomainEvent):
    encounter_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str


@dataclass(frozen=True, slots=True)
class EncounterDeleted(DomainEvent):
    encounter_id: UUID
    organization_id: UUID
