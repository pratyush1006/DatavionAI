"""
Master Patient Index merge reversal workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.mpi.constants import MPIMergeStatus
from apps.patient_management.mpi.events import MPIMergeReversedEvent
from apps.patient_management.mpi.models import MPIRecord
from apps.patient_management.mpi.policies import MPIPolicy
from apps.patient_management.mpi.services import MPIService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MPIReverseMergeRequest:
    """Input required to reverse an MPI merge."""

    organization_id: UUID
    duplicate_id: UUID


class MPIReverseMergeWorkflow(BaseWorkflow):
    """Orchestrate reversal of an MPI merge."""

    workflow_name = "patient_mpi.reverse_merge"

    def __init__(
        self,
        *,
        request: MPIReverseMergeRequest,
        policy: MPIPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the reverse merge workflow."""

        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MPIPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Reverse a merge and publish its event."""

        actor = User.objects.get(pk=context.actor_id)
        duplicate = MPIRecord.objects.select_related("organization").get(
            pk=self._request.duplicate_id,
            organization_id=self._request.organization_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_reverse_merge(actor=actor, record=duplicate):
            raise PermissionError(
                "You do not have permission to reverse MPI merges.",
            )

        duplicate = MPIService.reverse_merge(
            duplicate=duplicate,
            performed_by=actor,
        )

        self.publish_after_commit(
            MPIMergeReversedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                organization_id=duplicate.organization_id,
                record_id=duplicate.pk,
                merge_status=MPIMergeStatus.REVERSED,
            ),
        )

        return WorkflowResult.ok(
            context=context,
            data=duplicate,
            message="MPI merge reversed successfully.",
            code="patient_mpi_merge_reversed",
        )


__all__ = (
    "MPIReverseMergeRequest",
    "MPIReverseMergeWorkflow",
)
