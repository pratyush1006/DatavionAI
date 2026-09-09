"""
Patient Portal domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class PatientPortalAccountRestoredEvent(DomainEvent):
    """Emitted after a portal account is restored."""

    tenant_id: UUID
    actor_id: UUID
    account_id: UUID
    patient_id: UUID
    organization_id: UUID
