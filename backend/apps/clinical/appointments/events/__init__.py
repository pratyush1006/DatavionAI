"""Clinical Appointment domain events."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class AppointmentCreated(DomainEvent):
    """Describe an Appointment creation event."""

    appointment_id: UUID
    organization_id: UUID
    patient_id: UUID
    provider_id: UUID
    status: str


@dataclass(frozen=True)
class AppointmentUpdated(DomainEvent):
    """Describe an Appointment update event."""

    appointment_id: UUID
    organization_id: UUID


@dataclass(frozen=True)
class AppointmentDeleted(DomainEvent):
    """Describe an Appointment deletion event."""

    appointment_id: UUID
    organization_id: UUID


@dataclass(frozen=True)
class AppointmentStatusChanged(DomainEvent):
    """Describe an Appointment lifecycle event."""

    appointment_id: UUID
    organization_id: UUID
    previous_status: str
    status: str


__all__ = (
    "AppointmentCreated",
    "AppointmentDeleted",
    "AppointmentStatusChanged",
    "AppointmentUpdated",
)
