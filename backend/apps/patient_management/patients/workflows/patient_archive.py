"""
Patient archive workflow.
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
class PatientArchiveRequest:
    patient_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientArchiveData:
    patient_id: UUID
    archived: bool
    event_id: UUID | None = None


class PatientArchiveWorkflow(
    BaseWorkflow[PatientArchiveData],
):
    """
    Archive a Patient.

    Archiving is a lifecycle transition and is intentionally separate
    from physical/soft deletion.
    """

    def __init__(
        self,
        *,
        request: PatientArchiveRequest,
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
    ) -> WorkflowResult[PatientArchiveData]:
        from apps.platform.accounts.models import User

        actor = User.objects.get(
            id=context.actor_id,
        )

        patient = Patient.objects.get(
            id=self._request.patient_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_archive(
            actor=actor,
            patient=patient,
        ):
            raise PermissionError(
                "User does not have permission to archive patient.",
            )

        previous_status = patient.status

        if previous_status == PatientStatus.ARCHIVED:
            return WorkflowResult.ok(
                context=context,
                data=PatientArchiveData(
                    patient_id=patient.id,
                    archived=False,
                ),
                message="Patient is already archived.",
                code="patient_already_archived",
            )

        patient = PatientService.archive(
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
            "Patient archived.",
            extra={
                "patient_id": str(patient.id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientArchiveData(
                patient_id=patient.id,
                archived=True,
                event_id=event.event_id,
            ),
            message="Patient archived successfully.",
            code="patient_archived",
        )


__all__ = (
    "PatientArchiveData",
    "PatientArchiveRequest",
    "PatientArchiveWorkflow",
)
