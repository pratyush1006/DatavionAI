"""
Patient Portal domain event.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class PatientPortalAccountUpdatedEvent(DomainEvent):
    """Emitted after portal account metadata is updated."""

    tenant_id: UUID
    actor_id: UUID
    account_id: UUID
    patient_id: UUID
    organization_id: UUID
    changes: dict[str, Any]
