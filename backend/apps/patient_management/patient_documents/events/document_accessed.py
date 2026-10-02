"""Patient Document access-audited domain event."""

from __future__ import annotations

from uuid import UUID

from apps.core.events import DomainEvent


class PatientDocumentAccessedEvent(DomainEvent):
    """Describe one successful patient-document access operation."""

    event_type = "patient_document.accessed"

    def __init__(
        self,
        *,
        tenant_id: UUID,
        actor_id: UUID,
        document_id: UUID,
        patient_id: UUID,
        organization_id: UUID,
        action: str,
        access_log_id: UUID,
    ) -> None:
        """Initialize the access-audited domain event."""
        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "document_id": str(document_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
                "action": action,
                "access_log_id": str(access_log_id),
            },
        )


__all__ = ("PatientDocumentAccessedEvent",)
