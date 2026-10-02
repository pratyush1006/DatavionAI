"""Patient Communication domain event exports."""

from __future__ import annotations

from apps.patient_management.communication.events.created import (
    CommunicationCreatedEvent,
)
from apps.patient_management.communication.events.deleted import (
    CommunicationDeletedEvent,
)
from apps.patient_management.communication.events.restored import (
    CommunicationRestoredEvent,
)
from apps.patient_management.communication.events.status_changed import (
    CommunicationStatusChangedEvent,
)
from apps.patient_management.communication.events.updated import (
    CommunicationUpdatedEvent,
)

__all__ = (
    "CommunicationCreatedEvent",
    "CommunicationDeletedEvent",
    "CommunicationRestoredEvent",
    "CommunicationStatusChangedEvent",
    "CommunicationUpdatedEvent",
)
