"""
Master Patient Index lifecycle workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.mpi.events import MPIRecordStatusChangedEvent
from apps.patient_management.mpi.policies import MPIPolicy
from apps.patient_management.mpi.selectors import get_mpi_record
from apps.patient_management.mpi.services import MPIService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MPILifecycleRequest:
    """Input required for an MPI lifecycle transition."""

    organization_id: UUID
    record_id: UUID
    status: str


class MPILifecycleWorkflow(BaseWorkflow):
    """Orchestrate strict MPI lifecycle transitions."""

    workflow_name = "patient_mpi.lifecycle"

    def __init__(
        self,
        *,
        request: MPILifecycleRequest,
        policy: MPIPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the lifecycle workflow."""

        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MPIPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Transition an MPI record and publish its event."""

        actor = User.objects.get(pk=context.actor_id)
        record = get_mpi_record(
            tenant_id=context.tenant_id,
            organization_id=self._request.organization_id,
            record_id=self._request.record_id,
        )

        if not self._policy.can_transition(actor=actor, record=record):
            raise PermissionError(
                "You do not have permission to change MPI lifecycle state.",
            )

        previous_status = record.status
        record = MPIService.transition(
            record=record,
            status=self._request.status,
            performed_by=actor,
        )

        self.publish_after_commit(
            MPIRecordStatusChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                organization_id=record.organization_id,
                record_id=record.pk,
                previous_status=previous_status,
                status=record.status,
            ),
        )

        return WorkflowResult.ok(
            context=context,
            data=record,
            message="MPI record status changed successfully.",
            code="patient_mpi_status_changed",
        )


__all__ = (
    "MPILifecycleRequest",
    "MPILifecycleWorkflow",
)
