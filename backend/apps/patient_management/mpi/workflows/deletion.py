"""
Master Patient Index deletion workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.mpi.events import MPIRecordDeletedEvent
from apps.patient_management.mpi.policies import MPIPolicy
from apps.patient_management.mpi.selectors import get_mpi_record
from apps.patient_management.mpi.services import MPIService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MPIDeletionRequest:
    """Input required to soft-delete an MPI record."""

    organization_id: UUID
    record_id: UUID


class MPIDeletionWorkflow(BaseWorkflow):
    """Orchestrate MPI record soft deletion."""

    workflow_name = "patient_mpi.delete"

    def __init__(
        self,
        *,
        request: MPIDeletionRequest,
        policy: MPIPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the deletion workflow."""

        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MPIPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Soft-delete an MPI record and publish its event."""

        actor = User.objects.get(pk=context.actor_id)
        record = get_mpi_record(
            tenant_id=context.tenant_id,
            organization_id=self._request.organization_id,
            record_id=self._request.record_id,
        )

        if not self._policy.can_delete(actor=actor, record=record):
            raise PermissionError(
                "You do not have permission to delete MPI records.",
            )

        record = MPIService.delete_record(
            record=record,
            performed_by=actor,
        )

        self.publish_after_commit(
            MPIRecordDeletedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                organization_id=record.organization_id,
                record_id=record.pk,
            ),
        )

        return WorkflowResult.ok(
            context=context,
            data=record,
            message="MPI record deleted successfully.",
            code="patient_mpi_record_deleted",
        )


__all__ = (
    "MPIDeletionRequest",
    "MPIDeletionWorkflow",
)
