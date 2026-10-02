"""
Master Patient Index creation workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.mpi.events import MPIRecordCreatedEvent
from apps.patient_management.mpi.policies import MPIPolicy
from apps.patient_management.mpi.services import MPIService
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class MPICreationRequest:
    """Input required to create an MPI record."""

    organization_id: UUID
    patient_id: UUID
    data: dict


class MPICreationWorkflow(BaseWorkflow):
    """Orchestrate MPI record creation."""

    workflow_name = "patient_mpi.create"

    def __init__(
        self,
        *,
        request: MPICreationRequest,
        policy: MPIPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the creation workflow."""

        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MPIPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Create an MPI record and publish its event."""

        try:
            actor = User.objects.get(pk=context.actor_id)
            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
            patient = Patient.objects.select_related("organization").get(
                pk=self._request.patient_id,
                organization_id=organization.pk,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Organization, patient, or actor was not found.",
            ) from exc

        if not self._policy.can_create(actor=actor, organization=organization):
            raise PermissionError(
                "You do not have permission to create MPI records.",
            )

        record = MPIService.create_record(
            organization=organization,
            patient=patient,
            performed_by=actor,
            **self._request.data,
        )

        self.publish_after_commit(
            MPIRecordCreatedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                organization_id=record.organization_id,
                record_id=record.pk,
            ),
        )

        return WorkflowResult.ok(
            context=context,
            data=record,
            message="MPI record created successfully.",
            code="patient_mpi_record_created",
        )


__all__ = (
    "MPICreationRequest",
    "MPICreationWorkflow",
)
