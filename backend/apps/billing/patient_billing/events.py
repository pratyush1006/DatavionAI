"""Patient Billing domain events and post-commit publishing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.db import transaction

from apps.core.events.base import DomainEvent
from apps.core.events.publisher import publisher


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientBillingDomainEvent(DomainEvent):
    """Describe a Patient Billing aggregate change."""

    aggregate_id: UUID
    organization_id: UUID
    patient_id: UUID | None = None
    action: str
    changes: dict[str, Any] | None = None


def publish_after_commit(event: DomainEvent) -> None:
    """Publish a domain event only after the surrounding transaction commits."""

    transaction.on_commit(
        lambda: publisher.publish(event),
    )


__all__ = (
    "PatientBillingDomainEvent",
    "publish_after_commit",
)
