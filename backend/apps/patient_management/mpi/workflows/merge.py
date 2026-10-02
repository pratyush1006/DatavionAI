"""
Master Patient Index merge workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.mpi.constants import MPIMergeStatus
from apps.patient_management.mpi.events import MPIMergeCompletedEvent
from apps.patient_management.mpi.models import MPIMatchCandidate, MPIRecord
from apps.patient_management.mpi.policies import MPIPolicy
from apps.patient_management.mpi.services import MPIService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MPIMergeRequest:
    """Input required to merge two MPI records."""

    organization_id: UUID
    survivor_id: UUID
    duplicate_id: UUID
    candidate_id: UUID


class MPIMergeWorkflow(BaseWorkflow):
    """Orchestrate an administrative MPI merge backed by a confirmed match."""

    workflow_name = "patient_mpi.merge"

    def __init__(
        self,
        *,
        request: MPIMergeRequest,
        policy: MPIPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the merge workflow."""

        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MPIPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Merge a duplicate identity record without deleting Patient data."""

        actor = User.objects.get(pk=context.actor_id)
        records = MPIRecord.objects.select_related("organization").filter(
            organization_id=self._request.organization_id,
            organization__tenant_id=context.tenant_id,
            pk__in=(
                self._request.survivor_id,
                self._request.duplicate_id,
            ),
        )
        by_id = {record.pk: record for record in records}
        if set(by_id) != {
            self._request.survivor_id,
            self._request.duplicate_id,
        }:
            raise ValueError(
                "Both MPI records must exist in the selected organization and tenant.",
            )

        survivor = by_id[self._request.survivor_id]
        duplicate = by_id[self._request.duplicate_id]

        try:
            candidate = MPIMatchCandidate.objects.select_for_update().get(
                pk=self._request.candidate_id,
                organization_id=self._request.organization_id,
                organization__tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Confirmed MPI candidate was not found.") from exc

        if not self._policy.can_merge(
            actor=actor,
            organization=survivor.organization,
        ):
            raise PermissionError(
                "You do not have permission to merge MPI records.",
            )

        survivor, duplicate = MPIService.merge_records(
            survivor=survivor,
            duplicate=duplicate,
            candidate=candidate,
            performed_by=actor,
        )

        self.publish_after_commit(
            MPIMergeCompletedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                organization_id=survivor.organization_id,
                record_id=duplicate.pk,
                survivor_id=survivor.pk,
                merge_status=MPIMergeStatus.ACTIVE,
            ),
        )

        return WorkflowResult.ok(
            context=context,
            data=duplicate,
            message="MPI merge completed successfully.",
            code="patient_mpi_merge_completed",
        )


__all__ = (
    "MPIMergeRequest",
    "MPIMergeWorkflow",
)
