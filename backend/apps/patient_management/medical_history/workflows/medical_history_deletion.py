"""Medical History Deletion."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.medical_history.events import MedicalHistoryDeletedEvent
from apps.patient_management.medical_history.policies import MedicalHistoryPolicy
from apps.patient_management.medical_history.selectors import get_medical_history
from apps.patient_management.medical_history.services import delete_medical_history
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MedicalHistoryDeletionRequest:
    """MedicalHistoryDeletionRequest implementation."""

    history_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class MedicalHistoryDeletionData:
    """MedicalHistoryDeletionData implementation."""

    history_id: UUID
    patient_id: UUID
    organization_id: UUID
    deleted: bool
    event_id: UUID | None = None


class MedicalHistoryDeletionWorkflow(BaseWorkflow[MedicalHistoryDeletionData]):
    """MedicalHistoryDeletionWorkflow implementation."""

    workflow_name = "medical_history.delete"

    def __init__(
        self,
        *,
        request: MedicalHistoryDeletionRequest,
        policy: MedicalHistoryPolicy | None = None,
        logger_=None,
    ) -> None:
        """init  ."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MedicalHistoryPolicy()

    @transaction.atomic
    def _run(
        self, context: WorkflowContext
    ) -> WorkflowResult[MedicalHistoryDeletionData]:
        """run."""
        try:
            actor = User.objects.get(pk=context.actor_id)
            history = get_medical_history(
                tenant_id=context.tenant_id, history_id=self._request.history_id
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Medical history was not found.") from exc
        if not self._policy.can_delete(actor=actor, history=history):
            raise PermissionError(
                "You do not have permission to delete medical history."
            )
        delete_medical_history(instance=history, performed_by=actor)
        event = MedicalHistoryDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            history_id=history.pk,
            patient_id=history.patient_id,
            organization_id=history.organization_id,
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=MedicalHistoryDeletionData(
                history_id=history.pk,
                patient_id=history.patient_id,
                organization_id=history.organization_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Medical history deleted successfully.",
            code="medical_history_deleted",
        )


__all__ = (
    "MedicalHistoryDeletionRequest",
    "MedicalHistoryDeletionData",
    "MedicalHistoryDeletionWorkflow",
)
