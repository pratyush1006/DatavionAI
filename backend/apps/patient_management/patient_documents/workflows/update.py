"""Patient Document update workflow."""

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
    PatientDocumentUpdatedEvent,
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
class PatientDocumentUpdateRequest:
    """Input for Patient Document updates."""

    document_id: UUID
    data: Mapping[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDocumentUpdateData:
    """Successful Patient Document update result."""

    document_id: UUID
    updated: bool
    event_id: UUID | None = None


class PatientDocumentUpdateWorkflow(
    BaseWorkflow[PatientDocumentUpdateData],
):
    """Authorize and update a tenant-scoped patient document."""

    workflow_name = "patient_document.update"

    def __init__(
        self,
        *,
        request: PatientDocumentUpdateRequest,
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
    ) -> WorkflowResult[PatientDocumentUpdateData]:
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

        if not self._policy.can_update(
            actor=actor,
            document=document,
        ):
            raise PermissionError(
                "You do not have permission to update this patient document.",
            )

        updated = PatientDocumentService.update(
            instance=document,
            validated_data=self._request.data,
            performed_by=actor,
        )

        event = PatientDocumentUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            document_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientDocumentUpdateData(
                document_id=updated.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient document updated successfully.",
            code="patient_document_updated",
        )


__all__ = (
    "PatientDocumentUpdateData",
    "PatientDocumentUpdateRequest",
    "PatientDocumentUpdateWorkflow",
)
