"""
Patient activation workflow.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.patients.constants import (
    PatientStatus,
)
from apps.patient_management.patients.events import (
    PatientStatusChangedEvent,
)
from apps.patient_management.patients.models import (
    Patient,
)
from apps.patient_management.patients.policies import (
    PatientPolicy,
)
from apps.patient_management.patients.services import (
    PatientService,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientActivationRequest:
    patient_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientActivationData:
    patient_id: UUID
    activated: bool
    event_id: UUID | None = None


class PatientActivationWorkflow(
    BaseWorkflow[PatientActivationData],
):
    """
    Activate a Patient.
    """

    def __init__(
        self,
        *,
        request: PatientActivationRequest,
        policy: PatientPolicy | None = None,
        logger_: logging.Logger | None = None,
    ) -> None:
        super().__init__(
            logger_=logger_,
        )

        self._request = request
        self._policy = policy or PatientPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientActivationData]:
        from apps.platform.accounts.models import User

        actor = User.objects.get(
            id=context.actor_id,
        )

        patient = Patient.objects.get(
            id=self._request.patient_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_activate(
            actor=actor,
            patient=patient,
        ):
            raise PermissionError(
                "User does not have permission to activate patient.",
            )

        previous_status = patient.status

        if previous_status == PatientStatus.ACTIVE:
            return WorkflowResult.ok(
                context=context,
                data=PatientActivationData(
                    patient_id=patient.id,
                    activated=False,
                ),
                message="Patient is already active.",
                code="patient_already_active",
            )

        patient = PatientService.activate(
            instance=patient,
            actor=actor,
        )

        event = PatientStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            patient_id=patient.id,
            organization_id=patient.organization_id,
            previous_status=previous_status,
            new_status=patient.status,
        )

        self.publish_after_commit(event)

        logger.info(
            "Patient activated.",
            extra={
                "patient_id": str(patient.id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientActivationData(
                patient_id=patient.id,
                activated=True,
                event_id=event.event_id,
            ),
            message="Patient activated successfully.",
            code="patient_activated",
        )


__all__ = (
    "PatientActivationData",
    "PatientActivationRequest",
    "PatientActivationWorkflow",
)
