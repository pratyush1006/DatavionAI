"""Patient Document lifecycle workflows."""

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
    PatientDocumentRestoredEvent,
    PatientDocumentStatusChangedEvent,
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
class PatientDocumentLifecycleRequest:
    """Input for a lifecycle transition."""

    document_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDocumentLifecycleData:
    """Lifecycle workflow result."""

    document_id: UUID
    previous_status: str
    new_status: str
    event_id: UUID | None = None


class PatientDocumentActivationWorkflow(
    BaseWorkflow[PatientDocumentLifecycleData],
):
    """Activate a patient document."""

    workflow_name = "patient_document.activate"

    def __init__(
        self,
        *,
        request: PatientDocumentLifecycleRequest,
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
    ) -> WorkflowResult[PatientDocumentLifecycleData]:
        actor, document = _resolve(
            context,
            self._request.document_id,
        )
        if not self._policy.can_activate(
            actor=actor,
            document=document,
        ):
            raise PermissionError(
                "You do not have permission to activate this patient document.",
            )

        previous = document.status
        updated = PatientDocumentService.activate(
            instance=document,
            performed_by=actor,
        )
        event = PatientDocumentStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            document_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_status=previous,
            new_status=updated.status,
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=PatientDocumentLifecycleData(
                document_id=updated.id,
                previous_status=previous,
                new_status=updated.status,
                event_id=event.event_id,
            ),
            message="Patient document activated successfully.",
            code="patient_document_activated",
        )


class PatientDocumentArchiveWorkflow(
    BaseWorkflow[PatientDocumentLifecycleData],
):
    """Archive a patient document."""

    workflow_name = "patient_document.archive"

    def __init__(
        self,
        *,
        request: PatientDocumentLifecycleRequest,
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
    ) -> WorkflowResult[PatientDocumentLifecycleData]:
        actor, document = _resolve(
            context,
            self._request.document_id,
        )
        if not self._policy.can_archive(
            actor=actor,
            document=document,
        ):
            raise PermissionError(
                "You do not have permission to archive this patient document.",
            )

        previous = document.status
        updated = PatientDocumentService.archive(
            instance=document,
            performed_by=actor,
        )
        event = PatientDocumentStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            document_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_status=previous,
            new_status=updated.status,
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=PatientDocumentLifecycleData(
                document_id=updated.id,
                previous_status=previous,
                new_status=updated.status,
                event_id=event.event_id,
            ),
            message="Patient document archived successfully.",
            code="patient_document_archived",
        )


class PatientDocumentRestoreWorkflow(
    BaseWorkflow[PatientDocumentLifecycleData],
):
    """Restore a soft-deleted patient document."""

    workflow_name = "patient_document.restore"

    def __init__(
        self,
        *,
        request: PatientDocumentLifecycleRequest,
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
    ) -> WorkflowResult[PatientDocumentLifecycleData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            document = PatientDocument.all_objects.select_related(
                "organization",
                "patient",
            ).get(
                pk=self._request.document_id,
                organization__tenant_id=context.tenant_id,
                is_deleted=True,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Deleted patient document was not found.",
            ) from exc

        if not self._policy.can_restore(
            actor=actor,
            document=document,
        ):
            raise PermissionError(
                "You do not have permission to restore this patient document.",
            )

        previous = document.status
        restored = PatientDocumentService.restore(
            instance=document,
            performed_by=actor,
        )
        event = PatientDocumentRestoredEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            document_id=restored.id,
            patient_id=restored.patient_id,
            organization_id=restored.organization_id,
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=PatientDocumentLifecycleData(
                document_id=restored.id,
                previous_status=previous,
                new_status=restored.status,
                event_id=event.event_id,
            ),
            message="Patient document restored successfully.",
            code="patient_document_restored",
        )


def _resolve(
    context: WorkflowContext,
    document_id: UUID,
):
    """Resolve actor and active document within the tenant boundary."""
    try:
        actor = User.objects.get(
            pk=context.actor_id,
        )
        document = PatientDocument.objects.select_related(
            "organization",
            "patient",
        ).get(
            pk=document_id,
            organization__tenant_id=context.tenant_id,
        )
    except ObjectDoesNotExist as exc:
        raise ValueError(
            "Patient document was not found.",
        ) from exc
    return actor, document


__all__ = (
    "PatientDocumentActivationWorkflow",
    "PatientDocumentArchiveWorkflow",
    "PatientDocumentLifecycleData",
    "PatientDocumentLifecycleRequest",
    "PatientDocumentRestoreWorkflow",
)
