from dataclasses import dataclass
from uuid import UUID
from apps.core.events import DomainEvent

@dataclass(frozen=True, slots=True, kw_only=True)
class RecordingStartedEvent(DomainEvent):
    recording_id: UUID
    session_id: UUID
    organization_id: UUID

@dataclass(frozen=True, slots=True, kw_only=True)
class RecordingFinalizedEvent(DomainEvent):
    recording_id: UUID
    session_id: UUID
    organization_id: UUID
