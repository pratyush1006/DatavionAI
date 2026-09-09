"""Patient Document version creation workflow."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.patient_documents.events import (
    PatientDocumentVersionCreatedEvent,
)
from apps.patient_management.patient_documents.models import PatientDocument
from apps.patient_management.patient_documents.policies import PatientDocumentPolicy
from apps.patient_management.patient_documents.services import (
    PatientDocumentVersionService,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDocumentVersionCreationRequest:
    """Input for creation of one immutable document version."""

    document_id: UUID
    data: Mapping[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDocumentVersionCreationData:
    """Successful document-version creation result."""

    version: object
    event_id: UUID


class PatientDocumentVersionCreationWorkflow(
    BaseWorkflow[PatientDocumentVersionCreationData],
):
    """Authorize and create the next immutable document version."""

    workflow_name = "patient_document.version.create"

    def __init__(
        self,
        *,
        request: PatientDocumentVersionCreationRequest,
        policy: PatientDocumentPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the workflow."""
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
    ) -> WorkflowResult[PatientDocumentVersionCreationData]:
        """Execute version creation inside the tenant transaction."""
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

        if not self._policy.can_create_version(
            actor=actor,
            document=document,
        ):
            raise PermissionError(
                "You do not have permission to create document versions.",
            )

        version = PatientDocumentVersionService.create(
            patient_document=document,
            performed_by=actor,
            **dict(self._request.data),
        )
        event = PatientDocumentVersionCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            document_id=document.id,
            patient_id=document.patient_id,
            organization_id=document.organization_id,
            version_id=version.id,
            version_number=version.version_number,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientDocumentVersionCreationData(
                version=version,
                event_id=event.event_id,
            ),
            message="Patient document version created successfully.",
            code="patient_document_version_created",
        )


__all__ = (
    "PatientDocumentVersionCreationData",
    "PatientDocumentVersionCreationRequest",
    "PatientDocumentVersionCreationWorkflow",
)
