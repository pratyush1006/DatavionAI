"""
Patient deletion workflow.

Coordinates Patient deletion through the domain service.
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
    PatientDeletedEvent,
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
class PatientDeletionRequest:
    patient_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientDeletionData:
    patient_id: UUID
    deleted: bool
    event_id: UUID | None = None


class PatientDeletionWorkflow(
    BaseWorkflow[PatientDeletionData],
):
    """
    Delete a Patient through the Patient domain service.

    Patient deletion remains a workflow-level lifecycle operation;
    the underlying BaseModel/service determines whether the actual
    persistence operation is soft or hard deletion.
    """

    def __init__(
        self,
        *,
        request: PatientDeletionRequest,
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
    ) -> WorkflowResult[PatientDeletionData]:
        from apps.platform.accounts.models import User

        actor = User.objects.get(
            id=context.actor_id,
        )

        patient = Patient.objects.get(
            id=self._request.patient_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_delete(
            actor=actor,
            patient=patient,
        ):
            raise PermissionError(
                "User does not have permission to delete patient.",
            )

        if patient.status == PatientStatus.ACTIVE:
            raise ValueError(
                "Active patients must be deactivated or archived before deletion.",
            )

        patient_id = patient.id
        organization_id = patient.organization_id

        PatientService.delete(
            instance=patient,
            actor=actor,
        )

        event = PatientDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            patient_id=patient_id,
            organization_id=organization_id,
        )

        self.publish_after_commit(event)

        logger.info(
            "Patient deleted.",
            extra={
                "patient_id": str(patient_id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientDeletionData(
                patient_id=patient_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Patient deleted successfully.",
            code="patient_deleted",
        )


__all__ = (
    "PatientDeletionData",
    "PatientDeletionRequest",
    "PatientDeletionWorkflow",
)
