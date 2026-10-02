"""Patient Document creation workflow."""

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
    PatientDocumentCreatedEvent,
)
from apps.patient_management.patient_documents.policies import (
    PatientDocumentPolicy,
)
from apps.patient_management.patient_documents.services import (
    PatientDocumentService,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDocumentCreationRequest:
    """Input for Patient Document creation."""

    organization_id: UUID
    patient_id: UUID
    data: dict


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDocumentCreationData:
    """Successful Patient Document creation result."""

    document_id: UUID
    patient_id: UUID
    event_id: UUID


class PatientDocumentCreationWorkflow(
    BaseWorkflow[PatientDocumentCreationData],
):
    """Authorize and create a tenant-scoped Patient Document."""

    workflow_name = "patient_document.create"

    def __init__(
        self,
        *,
        request: PatientDocumentCreationRequest,
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
    ) -> WorkflowResult[PatientDocumentCreationData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            organization = Organization.objects.select_related("tenant").get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
            patient = Patient.objects.select_related("organization").get(
                pk=self._request.patient_id,
                organization_id=organization.id,
                organization__tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Organization or patient was not found.",
            ) from exc

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "You do not have permission to create patient documents.",
            )

        document = PatientDocumentService.create(
            organization=organization,
            patient=patient,
            performed_by=actor,
            **self._request.data,
        )

        event = PatientDocumentCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            document_id=document.id,
            patient_id=document.patient_id,
            organization_id=document.organization_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientDocumentCreationData(
                document_id=document.id,
                patient_id=document.patient_id,
                event_id=event.event_id,
            ),
            message="Patient document created successfully.",
            code="patient_document_created",
        )


__all__ = (
    "PatientDocumentCreationData",
    "PatientDocumentCreationRequest",
    "PatientDocumentCreationWorkflow",
)
