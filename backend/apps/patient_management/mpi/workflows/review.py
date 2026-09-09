"""
Master Patient Index candidate review workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.mpi.events import MPIMatchReviewedEvent
from apps.patient_management.mpi.models import MPIMatchCandidate
from apps.patient_management.mpi.policies import MPIPolicy
from apps.patient_management.mpi.services import MPIService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class MPIReviewRequest:
    """Input required to review an MPI candidate."""

    organization_id: UUID
    candidate_id: UUID
    status: str


class MPIReviewWorkflow(BaseWorkflow):
    """Orchestrate candidate match review."""

    workflow_name = "patient_mpi.review"

    def __init__(
        self,
        *,
        request: MPIReviewRequest,
        policy: MPIPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the review workflow."""

        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MPIPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Review a candidate and publish its event."""

        actor = User.objects.get(pk=context.actor_id)
        candidate = MPIMatchCandidate.objects.select_related("organization").get(
            pk=self._request.candidate_id,
            organization_id=self._request.organization_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_review(actor=actor, candidate=candidate):
            raise PermissionError(
                "You do not have permission to review MPI matches.",
            )

        candidate = MPIService.review_candidate(
            candidate=candidate,
            status=self._request.status,
            performed_by=actor,
        )

        self.publish_after_commit(
            MPIMatchReviewedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                organization_id=candidate.organization_id,
                candidate_id=candidate.pk,
                left_record_id=candidate.left_record_id,
                right_record_id=candidate.right_record_id,
            ),
        )

        return WorkflowResult.ok(
            context=context,
            data=candidate,
            message="MPI candidate reviewed successfully.",
            code="patient_mpi_match_reviewed",
        )


__all__ = (
    "MPIReviewRequest",
    "MPIReviewWorkflow",
)
