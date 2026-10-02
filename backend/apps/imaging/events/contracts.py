from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ImagingDomainEvent:
    event_type: str
    tenant_id: UUID
    entity_type: str
    entity_id: UUID
    correlation_id: UUID
    payload: dict
