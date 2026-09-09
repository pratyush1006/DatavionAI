"""
Patient domain events.

Public event API for the Patient bounded context.
"""

from __future__ import annotations

from apps.patient_management.patients.events.patient_created import (
    PatientCreatedEvent,
)
from apps.patient_management.patients.events.patient_deleted import (
    PatientDeletedEvent,
)
from apps.patient_management.patients.events.patient_status_changed import (
    PatientStatusChangedEvent,
)
from apps.patient_management.patients.events.patient_updated import (
    PatientUpdatedEvent,
)

__all__: tuple[str, ...] = (
    "PatientCreatedEvent",
    "PatientDeletedEvent",
    "PatientStatusChangedEvent",
    "PatientUpdatedEvent",
)
