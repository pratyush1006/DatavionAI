"""Patient Document deletion workflow."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.patient_documents.events import (
    PatientDocumentDeletedEvent,
)
from apps.patient_management.patient_documents.models import (
    PatientDocument,
)
from apps.patient_management.patient_documents.policies import (
    PatientDocumentPolicy,
)
from apps.patient_management.patient_documents.services import (
    PatientDocumentService,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDocumentDeletionRequest:
    """Input for Patient Document deletion."""

    document_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDocumentDeletionData:
    """Successful Patient Document deletion result."""

    document_id: UUID
    deleted: bool
    event_id: UUID


class PatientDocumentDeletionWorkflow(
    BaseWorkflow[PatientDocumentDeletionData],
):
    """Soft-delete a tenant-scoped patient document."""

    workflow_name = "patient_document.delete"

    def __init__(
        self,
        *,
        request: PatientDocumentDeletionRequest,
        policy: PatientDocumentPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientDocumentPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientDocumentDeletionData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            document = PatientDocument.objects.select_related(
                "organization",
                "patient",
            ).get(
                pk=self._request.document_id,
                organization__tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient document was not found.",
            ) from exc

        if not self._policy.can_delete(
            actor=actor,
            document=document,
        ):
            raise PermissionError(
                "You do not have permission to delete this patient document.",
            )

        PatientDocumentService.delete(
            instance=document,
            performed_by=actor,
        )

        event = PatientDocumentDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            document_id=document.id,
            patient_id=document.patient_id,
            organization_id=document.organization_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientDocumentDeletionData(
                document_id=document.id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Patient document deleted successfully.",
            code="patient_document_deleted",
        )


__all__ = (
    "PatientDocumentDeletionData",
    "PatientDocumentDeletionRequest",
    "PatientDocumentDeletionWorkflow",
)
