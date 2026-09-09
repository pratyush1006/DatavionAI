"""Patient Document access-audit workflow."""

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
    PatientDocumentAccessedEvent,
)
from apps.patient_management.patient_documents.models import PatientDocument
from apps.patient_management.patient_documents.policies import (
    PatientDocumentPolicy,
)
from apps.patient_management.patient_documents.services import (
    PatientDocumentAccessLogService,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDocumentAccessRequest:
    """Input required to record one document access operation."""

    document_id: UUID
    action: str
    ip_address: str | None = None
    user_agent: str = ""
    metadata: Mapping[str, Any] | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDocumentAccessData:
    """Successful document-access workflow result."""

    access_log: object
    event_id: UUID


class PatientDocumentAccessWorkflow(
    BaseWorkflow[PatientDocumentAccessData],
):
    """Authorize, audit, and publish one document access operation."""

    workflow_name = "patient_document.access"

    def __init__(
        self,
        *,
        request: PatientDocumentAccessRequest,
        policy: PatientDocumentPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the access workflow."""
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
    ) -> WorkflowResult[PatientDocumentAccessData]:
        """Record access after tenant and object authorization."""
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

        if not self._policy.can_view(
            actor=actor,
            document=document,
        ):
            raise PermissionError(
                "You do not have permission to view patient documents.",
            )

        access_log = PatientDocumentAccessLogService.record(
            patient_document=document,
            user=actor,
            action=self._request.action,
            ip_address=self._request.ip_address,
            user_agent=self._request.user_agent,
            metadata=dict(self._request.metadata or {}),
        )
        event = PatientDocumentAccessedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            document_id=document.id,
            patient_id=document.patient_id,
            organization_id=document.organization_id,
            action=self._request.action,
            access_log_id=access_log.id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientDocumentAccessData(
                access_log=access_log,
                event_id=event.event_id,
            ),
            message="Patient document access recorded successfully.",
            code="patient_document_access_recorded",
        )


__all__ = (
    "PatientDocumentAccessData",
    "PatientDocumentAccessRequest",
    "PatientDocumentAccessWorkflow",
)
