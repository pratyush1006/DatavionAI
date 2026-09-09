"""Medical History Verification."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.medical_history.events import MedicalHistoryVerifiedEvent
from apps.patient_management.medical_history.policies import MedicalHistoryPolicy
from apps.patient_management.medical_history.selectors import get_medical_history
from apps.patient_management.medical_history.services import verify_medical_history
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MedicalHistoryVerificationRequest:
    """MedicalHistoryVerificationRequest implementation."""

    history_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class MedicalHistoryVerificationData:
    """MedicalHistoryVerificationData implementation."""

    history_id: UUID
    patient_id: UUID
    organization_id: UUID
    verified: bool
    event_id: UUID | None = None


class MedicalHistoryVerificationWorkflow(BaseWorkflow[MedicalHistoryVerificationData]):
    """MedicalHistoryVerificationWorkflow implementation."""

    workflow_name = "medical_history.verify"

    def __init__(
        self,
        *,
        request: MedicalHistoryVerificationRequest,
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
    ) -> WorkflowResult[MedicalHistoryVerificationData]:
        """run."""
        try:
            actor = User.objects.get(pk=context.actor_id)
            history = get_medical_history(
                tenant_id=context.tenant_id, history_id=self._request.history_id
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Medical history was not found.") from exc
        if not self._policy.can_verify(actor=actor, history=history):
            raise PermissionError(
                "You do not have permission to verify medical history."
            )
        if history.is_verified:
            return WorkflowResult.ok(
                context=context,
                data=MedicalHistoryVerificationData(
                    history_id=history.pk,
                    patient_id=history.patient_id,
                    organization_id=history.organization_id,
                    verified=True,
                ),
                message="Medical history is already verified.",
                code="medical_history_already_verified",
            )
        history = verify_medical_history(instance=history, performed_by=actor)
        event = MedicalHistoryVerifiedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            history_id=history.pk,
            patient_id=history.patient_id,
            organization_id=history.organization_id,
            verified_at=history.verified_at.isoformat() if history.verified_at else "",
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=MedicalHistoryVerificationData(
                history_id=history.pk,
                patient_id=history.patient_id,
                organization_id=history.organization_id,
                verified=True,
                event_id=event.event_id,
            ),
            message="Medical history verified successfully.",
            code="medical_history_verified",
        )


__all__ = (
    "MedicalHistoryVerificationRequest",
    "MedicalHistoryVerificationData",
    "MedicalHistoryVerificationWorkflow",
)
