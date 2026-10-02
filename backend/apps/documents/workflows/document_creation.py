"""
Document creation workflow.

Coordinates document creation process.

Responsibilities:

- Resolve tenant context
- Resolve organization
- Execute document service
- Publish domain event
- Dispatch post commit tasks
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.documents.events import (
    DocumentCreatedEvent,
)
from apps.documents.services import (
    create_document,
)
from apps.documents.tasks import (
    index_document,
    send_document_created_notification,
    synchronize_document,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DocumentCreationRequest:
    """
    Document creation request.
    """

    organization_id: UUID

    title: str

    storage_key: str

    document_type: str

    original_filename: str | None = None

    mime_type: str | None = None

    file_size: int = 0

    checksum: str | None = None

    metadata: dict | None = None

    ai_metadata: dict | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DocumentCreationData:
    """
    Document creation result.
    """

    document_id: UUID

    created: bool

    event_id: UUID | None = None


class DocumentCreationWorkflow(
    BaseWorkflow[DocumentCreationData],
):
    """
    Creates document.

    Flow:

        Context
          |
          v
        Organization
          |
          v
        Domain Service
          |
          v
        Domain Event
          |
          v
        Async Tasks
    """

    def __init__(
        self,
        *,
        request: DocumentCreationRequest,
    ) -> None:

        super().__init__()

        self._request = request

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[DocumentCreationData]:
        """
        Execute document creation.
        """

        from apps.platform.organizations.models import (
            Organization,
        )

        organization = Organization.objects.get(
            id=self._request.organization_id,
        )

        document = create_document(
            tenant_id=context.tenant_id,
            organization_id=organization.id,
            title=self._request.title,
            storage_key=self._request.storage_key,
            document_type=self._request.document_type,
            original_filename=(self._request.original_filename or ""),
            mime_type=(self._request.mime_type or ""),
            file_size=self._request.file_size,
            checksum=(self._request.checksum or ""),
            metadata=(self._request.metadata or {}),
            ai_metadata=(self._request.ai_metadata or {}),
        )

        event = DocumentCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            document_id=document.id,
            organization_id=organization.id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            index_document,
            document_id=document.id,
        )

        self.dispatch_after_commit(
            synchronize_document,
            document_id=document.id,
        )

        self.dispatch_after_commit(
            send_document_created_notification,
            document_id=document.id,
        )

        logger.info(
            "Document created.",
            extra={
                "document_id": str(
                    document.id,
                ),
                "tenant_id": str(
                    context.tenant_id,
                ),
                "actor_id": str(
                    context.actor_id,
                ),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=DocumentCreationData(
                document_id=document.id,
                created=True,
                event_id=event.event_id,
            ),
            message=("Document created successfully."),
            code="document_created",
        )


__all__ = (
    "DocumentCreationRequest",
    "DocumentCreationData",
    "DocumentCreationWorkflow",
)
