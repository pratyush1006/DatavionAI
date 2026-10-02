"""
Master Patient Index restore workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.mpi.models import MPIRecord
from apps.patient_management.mpi.policies import MPIPolicy
from apps.patient_management.mpi.services import MPIService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MPIRestoreRequest:
    """Input required to restore an MPI record."""

    organization_id: UUID
    record_id: UUID


class MPIRestoreWorkflow(BaseWorkflow):
    """Orchestrate restoration of an MPI record."""

    workflow_name = "patient_mpi.restore"

    def __init__(
        self,
        *,
        request: MPIRestoreRequest,
        policy: MPIPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the restore workflow."""

        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MPIPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Restore a deleted MPI record."""

        actor = User.objects.get(pk=context.actor_id)
        record = MPIRecord.all_objects.select_related("organization").get(
            pk=self._request.record_id,
            organization_id=self._request.organization_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_restore(actor=actor, record=record):
            raise PermissionError(
                "You do not have permission to restore MPI records.",
            )

        record = MPIService.restore_record(
            record=record,
            performed_by=actor,
        )

        return WorkflowResult.ok(
            context=context,
            data=record,
            message="MPI record restored successfully.",
            code="patient_mpi_record_restored",
        )


__all__ = (
    "MPIRestoreRequest",
    "MPIRestoreWorkflow",
)
