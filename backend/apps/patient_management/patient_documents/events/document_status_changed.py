"""Patient Document lifecycle domain event."""

from __future__ import annotations

from uuid import UUID

from apps.core.events import DomainEvent


class PatientDocumentStatusChangedEvent(DomainEvent):
    """Describe a patient document lifecycle transition."""

    event_type = "patient_document.status_changed"

    def __init__(
        self,
        *,
        tenant_id: UUID,
        actor_id: UUID,
        document_id: UUID,
        patient_id: UUID,
        organization_id: UUID,
        previous_status: str,
        new_status: str,
    ) -> None:
        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "document_id": str(document_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
                "previous_status": previous_status,
                "new_status": new_status,
            },
        )


__all__ = ("PatientDocumentStatusChangedEvent",)
