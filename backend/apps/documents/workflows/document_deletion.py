"""Tenant-bound Document deletion workflow."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.documents.events import DocumentDeletedEvent
from apps.documents.selectors import get_document_by_id_for_tenant
from apps.documents.services import delete_document
from apps.documents.tasks import (
    index_document,
    send_document_deleted_notification,
    synchronize_document,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentDeletionRequest:
    document_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentDeletionData:
    document_id: UUID
    deleted: bool
    event_id: UUID | None = None


class DocumentDeletionWorkflow(BaseWorkflow[DocumentDeletionData]):
    def __init__(self, *, request: DocumentDeletionRequest) -> None:
        super().__init__()
        self._request = request

    def _run(self, *, context: WorkflowContext) -> WorkflowResult[DocumentDeletionData]:
        if context.tenant_id is None:
            return WorkflowResult.fail(
                context=context,
                message="A tenant context is required.",
                code="document_tenant_context_required",
            )
        document = get_document_by_id_for_tenant(
            document_id=self._request.document_id, tenant_id=context.tenant_id
        )
        deleted_document = delete_document(instance=document)
        event = DocumentDeletedEvent(
            tenant_id=deleted_document.tenant_id,
            actor_id=context.actor_id,
            document_id=deleted_document.id,
            organization_id=deleted_document.organization_id,
        )
        self.publish_after_commit(event)
        self.dispatch_after_commit(index_document, document_id=deleted_document.id)
        self.dispatch_after_commit(
            synchronize_document, document_id=deleted_document.id
        )
        self.dispatch_after_commit(
            send_document_deleted_notification, document_id=deleted_document.id
        )
        logger.info(
            "Document deleted.",
            extra={
                "document_id": str(deleted_document.id),
                "tenant_id": str(deleted_document.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )
        return WorkflowResult.ok(
            context=context,
            data=DocumentDeletionData(
                document_id=deleted_document.id, deleted=True, event_id=event.event_id
            ),
            message="Document deleted successfully.",
            code="document_deleted",
        )


__all__ = (
    "DocumentDeletionRequest",
    "DocumentDeletionData",
    "DocumentDeletionWorkflow",
)
