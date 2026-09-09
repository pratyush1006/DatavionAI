"""Patient Document updated domain event."""

from __future__ import annotations

from uuid import UUID

from apps.core.events import DomainEvent


class PatientDocumentUpdatedEvent(DomainEvent):
    """Describe metadata mutation of a patient document."""

    event_type = "patient_document.updated"

    def __init__(
        self,
        *,
        tenant_id: UUID,
        actor_id: UUID,
        document_id: UUID,
        patient_id: UUID,
        organization_id: UUID,
    ) -> None:
        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "document_id": str(document_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
            },
        )


__all__ = ("PatientDocumentUpdatedEvent",)
