from dataclasses import dataclass
from uuid import UUID

from apps.core.events import DomainEvent


@dataclass(frozen=True, slots=True)
class PatientRelationshipVerifiedEvent(DomainEvent):
    tenant_id: UUID
    actor_id: UUID
    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
