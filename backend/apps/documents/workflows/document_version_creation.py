"""
Document version creation workflow.

Coordinates document version lifecycle.

Responsibilities:

- Resolve document
- Execute version creation service
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
    DocumentVersionCreatedEvent,
)
from apps.documents.selectors import (
    get_document_by_id,
)
from apps.documents.services import (
    create_document_version,
)
from apps.documents.tasks import (
    index_document,
    synchronize_document,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DocumentVersionCreationRequest:
    """
    Document version creation request.
    """

    document_id: UUID

    storage_key: str

    version_number: int

    original_filename: str | None = None

    mime_type: str | None = None

    file_size: int = 0

    checksum: str | None = None

    metadata: dict | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DocumentVersionCreationData:
    """
    Document version creation result.
    """

    document_id: UUID

    version_id: UUID

    created: bool

    event_id: UUID | None = None


class DocumentVersionCreationWorkflow(
    BaseWorkflow[DocumentVersionCreationData],
):
    """
    Creates document version.

    Flow:

        Context
          |
          v
        Document Selector
          |
          v
        Version Service
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
        request: DocumentVersionCreationRequest,
    ) -> None:

        super().__init__()

        self._request = request

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[DocumentVersionCreationData]:
        """
        Execute document version creation.
        """

        document = get_document_by_id(
            document_id=(self._request.document_id),
        )

        version = create_document_version(
            document_id=document.id,
            storage_key=(self._request.storage_key),
            version_number=(self._request.version_number),
            uploaded_by_id=(context.actor_id),
            original_filename=(self._request.original_filename or ""),
            mime_type=(self._request.mime_type or ""),
            file_size=(self._request.file_size),
            checksum=(self._request.checksum or ""),
            metadata=(self._request.metadata or {}),
        )

        event = DocumentVersionCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            document_id=document.id,
            version_id=version.id,
            organization_id=(document.organization_id),
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

        logger.info(
            "Document version created.",
            extra={
                "document_id": str(
                    document.id,
                ),
                "version_id": str(
                    version.id,
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
            data=DocumentVersionCreationData(
                document_id=document.id,
                version_id=version.id,
                created=True,
                event_id=event.event_id,
            ),
            message=("Document version created successfully."),
            code="document_version_created",
        )


__all__ = (
    "DocumentVersionCreationRequest",
    "DocumentVersionCreationData",
    "DocumentVersionCreationWorkflow",
)
