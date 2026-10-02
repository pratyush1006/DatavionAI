"""Medical History Update."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.medical_history.events import MedicalHistoryUpdatedEvent
from apps.patient_management.medical_history.policies import MedicalHistoryPolicy
from apps.patient_management.medical_history.selectors import get_medical_history
from apps.patient_management.medical_history.services import update_medical_history
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MedicalHistoryUpdateRequest:
    """MedicalHistoryUpdateRequest implementation."""

    history_id: UUID
    data: dict


@dataclass(frozen=True, slots=True, kw_only=True)
class MedicalHistoryUpdateData:
    """MedicalHistoryUpdateData implementation."""

    history_id: UUID
    patient_id: UUID
    organization_id: UUID
    updated: bool
    event_id: UUID | None = None


class MedicalHistoryUpdateWorkflow(BaseWorkflow[MedicalHistoryUpdateData]):
    """MedicalHistoryUpdateWorkflow implementation."""

    workflow_name = "medical_history.update"

    def __init__(
        self,
        *,
        request: MedicalHistoryUpdateRequest,
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
    ) -> WorkflowResult[MedicalHistoryUpdateData]:
        """run."""
        try:
            actor = User.objects.get(pk=context.actor_id)
            history = get_medical_history(
                tenant_id=context.tenant_id, history_id=self._request.history_id
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Medical history was not found.") from exc
        if not self._policy.can_update(actor=actor, history=history):
            raise PermissionError(
                "You do not have permission to update medical history."
            )
        changes = dict(self._request.data)
        if not changes:
            return WorkflowResult.ok(
                context=context,
                data=MedicalHistoryUpdateData(
                    history_id=history.pk,
                    patient_id=history.patient_id,
                    organization_id=history.organization_id,
                    updated=False,
                ),
                message="No changes were supplied.",
                code="medical_history_unchanged",
            )
        updated = update_medical_history(
            instance=history, validated_data=changes, performed_by=actor
        )
        event = MedicalHistoryUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            history_id=updated.pk,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            changes=changes,
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=MedicalHistoryUpdateData(
                history_id=updated.pk,
                patient_id=updated.patient_id,
                organization_id=updated.organization_id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Medical history updated successfully.",
            code="medical_history_updated",
        )


__all__ = (
    "MedicalHistoryUpdateRequest",
    "MedicalHistoryUpdateData",
    "MedicalHistoryUpdateWorkflow",
)
