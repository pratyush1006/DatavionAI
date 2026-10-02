from dataclasses import dataclass
from uuid import UUID
from apps.core.events import DomainEvent

@dataclass(frozen=True, slots=True, kw_only=True)
class ParticipantStatusChangedEvent(DomainEvent):
    participant_id: UUID
    session_id: UUID
    organization_id: UUID
    previous_status: str = ""
    status: str = ""

@dataclass(frozen=True, slots=True, kw_only=True)
class ParticipantMediaStateChangedEvent(DomainEvent):
    participant_id: UUID
    session_id: UUID
    organization_id: UUID
    microphone_enabled: bool
    camera_enabled: bool
    audio_connected: bool
    video_connected: bool
