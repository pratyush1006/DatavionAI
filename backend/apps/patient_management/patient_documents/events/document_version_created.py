"""Patient Document version-created domain event."""

from __future__ import annotations

from uuid import UUID

from apps.core.events import DomainEvent


class PatientDocumentVersionCreatedEvent(DomainEvent):
    """Describe creation of one immutable document version."""

    event_type = "patient_document.version_created"

    def __init__(
        self,
        *,
        tenant_id: UUID,
        actor_id: UUID,
        document_id: UUID,
        patient_id: UUID,
        organization_id: UUID,
        version_id: UUID,
        version_number: int,
    ) -> None:
        """Initialize the version-created event."""
        super().__init__(
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload={
                "document_id": str(document_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
                "version_id": str(version_id),
                "version_number": version_number,
            },
        )


__all__ = ("PatientDocumentVersionCreatedEvent",)
