"""
Domain event exports for Patient Consents.
"""

from __future__ import annotations

from .created import (
    PatientConsentCreatedEvent,
)
from .deleted import (
    PatientConsentDeletedEvent,
)
from .status_changed import (
    PatientConsentStatusChangedEvent,
)
from .updated import (
    PatientConsentUpdatedEvent,
)

__all__ = (
    "PatientConsentCreatedEvent",
    "PatientConsentDeletedEvent",
    "PatientConsentStatusChangedEvent",
    "PatientConsentUpdatedEvent",
)
