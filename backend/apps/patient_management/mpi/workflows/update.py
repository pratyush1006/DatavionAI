"""
Master Patient Index update workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.mpi.events import MPIRecordUpdatedEvent
from apps.patient_management.mpi.policies import MPIPolicy
from apps.patient_management.mpi.selectors import get_mpi_record
from apps.patient_management.mpi.services import MPIService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MPIUpdateRequest:
    """Input required to update an MPI record."""

    organization_id: UUID
    record_id: UUID
    data: dict


class MPIUpdateWorkflow(BaseWorkflow):
    """Orchestrate MPI metadata updates."""

    workflow_name = "patient_mpi.update"

    def __init__(
        self,
        *,
        request: MPIUpdateRequest,
        policy: MPIPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the update workflow."""

        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MPIPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Update the record and publish its event."""

        actor = User.objects.get(pk=context.actor_id)
        record = get_mpi_record(
            tenant_id=context.tenant_id,
            organization_id=self._request.organization_id,
            record_id=self._request.record_id,
        )

        if not self._policy.can_update(actor=actor, record=record):
            raise PermissionError(
                "You do not have permission to update MPI records.",
            )

        record = MPIService.update_record(
            record=record,
            data=self._request.data,
            performed_by=actor,
        )

        self.publish_after_commit(
            MPIRecordUpdatedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                organization_id=record.organization_id,
                record_id=record.pk,
            ),
        )

        return WorkflowResult.ok(
            context=context,
            data=record,
            message="MPI record updated successfully.",
            code="patient_mpi_record_updated",
        )


__all__ = (
    "MPIUpdateRequest",
    "MPIUpdateWorkflow",
)
