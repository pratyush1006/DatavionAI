"""Medical History Lifecycle."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.medical_history.events import (
    MedicalHistoryStatusChangedEvent,
)
from apps.patient_management.medical_history.policies import MedicalHistoryPolicy
from apps.patient_management.medical_history.selectors import (
    get_deleted_medical_history,
    get_medical_history,
)
from apps.patient_management.medical_history.services import (
    activate_medical_history,
    deactivate_medical_history,
    restore_medical_history,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MedicalHistoryLifecycleRequest:
    """MedicalHistoryLifecycleRequest implementation."""

    history_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class MedicalHistoryLifecycleData:
    """MedicalHistoryLifecycleData implementation."""

    history_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str
    restored: bool = False
    activated: bool = False
    deactivated: bool = False
    event_id: UUID | None = None


def _result(*, context, history, previous, event, message, code, **flags):
    """result."""
    return WorkflowResult.ok(
        context=context,
        data=MedicalHistoryLifecycleData(
            history_id=history.pk,
            patient_id=history.patient_id,
            organization_id=history.organization_id,
            previous_status=previous,
            new_status=history.clinical_status,
            event_id=event.event_id,
            **flags,
        ),
        message=message,
        code=code,
    )


class MedicalHistoryRestoreWorkflow(BaseWorkflow[MedicalHistoryLifecycleData]):
    """MedicalHistoryRestoreWorkflow implementation."""

    workflow_name = "medical_history.restore"

    def __init__(
        self,
        *,
        request: MedicalHistoryLifecycleRequest,
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
    ) -> WorkflowResult[MedicalHistoryLifecycleData]:
        """run."""
        try:
            actor = User.objects.get(pk=context.actor_id)
            history = get_deleted_medical_history(
                tenant_id=context.tenant_id, history_id=self._request.history_id
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Deleted medical history was not found.") from exc
        if not self._policy.can_restore(actor=actor, history=history):
            raise PermissionError(
                "You do not have permission to restore medical history."
            )
        previous = history.clinical_status
        history = restore_medical_history(instance=history, performed_by=actor)
        event = MedicalHistoryStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            history_id=history.pk,
            patient_id=history.patient_id,
            organization_id=history.organization_id,
            previous_status=previous,
            new_status=history.clinical_status,
        )
        self.publish_after_commit(event)
        return _result(
            context=context,
            history=history,
            previous=previous,
            event=event,
            message="Medical history restored successfully.",
            code="medical_history_restored",
            restored=True,
        )


class MedicalHistoryActivationWorkflow(BaseWorkflow[MedicalHistoryLifecycleData]):
    """MedicalHistoryActivationWorkflow implementation."""

    workflow_name = "medical_history.activate"

    def __init__(
        self,
        *,
        request: MedicalHistoryLifecycleRequest,
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
    ) -> WorkflowResult[MedicalHistoryLifecycleData]:
        """run."""
        try:
            actor = User.objects.get(pk=context.actor_id)
            history = get_medical_history(
                tenant_id=context.tenant_id, history_id=self._request.history_id
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Medical history was not found.") from exc
        if not self._policy.can_activate(actor=actor, history=history):
            raise PermissionError(
                "You do not have permission to activate medical history."
            )
        previous = history.clinical_status
        history = activate_medical_history(instance=history, performed_by=actor)
        event = MedicalHistoryStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            history_id=history.pk,
            patient_id=history.patient_id,
            organization_id=history.organization_id,
            previous_status=previous,
            new_status=history.clinical_status,
        )
        self.publish_after_commit(event)
        return _result(
            context=context,
            history=history,
            previous=previous,
            event=event,
            message="Medical history activated successfully.",
            code="medical_history_activated",
            activated=True,
        )


class MedicalHistoryDeactivationWorkflow(BaseWorkflow[MedicalHistoryLifecycleData]):
    """MedicalHistoryDeactivationWorkflow implementation."""

    workflow_name = "medical_history.deactivate"

    def __init__(
        self,
        *,
        request: MedicalHistoryLifecycleRequest,
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
    ) -> WorkflowResult[MedicalHistoryLifecycleData]:
        """run."""
        try:
            actor = User.objects.get(pk=context.actor_id)
            history = get_medical_history(
                tenant_id=context.tenant_id, history_id=self._request.history_id
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Medical history was not found.") from exc
        if not self._policy.can_deactivate(actor=actor, history=history):
            raise PermissionError(
                "You do not have permission to deactivate medical history."
            )
        previous = history.clinical_status
        history = deactivate_medical_history(instance=history, performed_by=actor)
        event = MedicalHistoryStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            history_id=history.pk,
            patient_id=history.patient_id,
            organization_id=history.organization_id,
            previous_status=previous,
            new_status=history.clinical_status,
        )
        self.publish_after_commit(event)
        return _result(
            context=context,
            history=history,
            previous=previous,
            event=event,
            message="Medical history deactivated successfully.",
            code="medical_history_deactivated",
            deactivated=True,
        )


__all__ = (
    "MedicalHistoryLifecycleRequest",
    "MedicalHistoryLifecycleData",
    "MedicalHistoryRestoreWorkflow",
    "MedicalHistoryActivationWorkflow",
    "MedicalHistoryDeactivationWorkflow",
)
