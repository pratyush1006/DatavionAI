"""
Patient created domain event.

Published after a patient aggregate has been successfully created
and the surrounding database transaction has committed.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientCreatedEvent(DomainEvent):
    """
    Emitted when a patient is created.
    """

    tenant_id: UUID
    actor_id: UUID
    patient_id: UUID
    organization_id: UUID


__all__: tuple[str, ...] = ("PatientCreatedEvent",)
