from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True)
class InsuranceEntityChanged(DomainEvent):
    entity_type: str
    action: str
    organization_id: UUID


__all__ = ("InsuranceEntityChanged",)
