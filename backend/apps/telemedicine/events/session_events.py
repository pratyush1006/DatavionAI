from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True, kw_only=True)
class SessionCreatedEvent(DomainEvent):
    session_id: UUID
    organization_id: UUID
    patient_id: UUID
    provider_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class SessionStatusChangedEvent(DomainEvent):
    session_id: UUID
    organization_id: UUID
    previous_status: str = ""
    status: str = ""
