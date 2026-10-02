"""Tenant-bound Document update workflow."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.documents.events import DocumentUpdatedEvent
from apps.documents.selectors import get_document_by_id_for_tenant
from apps.documents.services import update_document
from apps.documents.tasks import (
    index_document,
    send_document_updated_notification,
    synchronize_document,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentUpdateRequest:
    document_id: UUID
    data: dict


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentUpdateData:
    document_id: UUID
    updated: bool
    event_id: UUID | None = None


class DocumentUpdateWorkflow(BaseWorkflow[DocumentUpdateData]):
    def __init__(self, *, request: DocumentUpdateRequest) -> None:
        super().__init__()
        self._request = request

    def _run(self, *, context: WorkflowContext) -> WorkflowResult[DocumentUpdateData]:
        if context.tenant_id is None:
            return WorkflowResult.fail(
                context=context,
                message="A tenant context is required.",
                code="document_tenant_context_required",
            )
        document = get_document_by_id_for_tenant(
            document_id=self._request.document_id, tenant_id=context.tenant_id
        )
        updated_document = update_document(instance=document, data=self._request.data)
        event = DocumentUpdatedEvent(
            tenant_id=updated_document.tenant_id,
            actor_id=context.actor_id,
            document_id=updated_document.id,
            organization_id=updated_document.organization_id,
        )
        self.publish_after_commit(event)
        self.dispatch_after_commit(index_document, document_id=updated_document.id)
        self.dispatch_after_commit(
            synchronize_document, document_id=updated_document.id
        )
        self.dispatch_after_commit(
            send_document_updated_notification, document_id=updated_document.id
        )
        logger.info(
            "Document updated.",
            extra={
                "document_id": str(updated_document.id),
                "tenant_id": str(updated_document.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )
        return WorkflowResult.ok(
            context=context,
            data=DocumentUpdateData(
                document_id=updated_document.id, updated=True, event_id=event.event_id
            ),
            message="Document updated successfully.",
            code="document_updated",
        )


__all__ = ("DocumentUpdateRequest", "DocumentUpdateData", "DocumentUpdateWorkflow")
