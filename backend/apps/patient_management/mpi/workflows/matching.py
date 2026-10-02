"""
Master Patient Index candidate matching workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.mpi.events import MPIMatchCreatedEvent
from apps.patient_management.mpi.models import MPIRecord
from apps.patient_management.mpi.policies import MPIPolicy
from apps.patient_management.mpi.services import MPIService
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class MPIMatchingRequest:
    """Input required to generate an MPI candidate match."""

    organization_id: UUID
    left_record_id: UUID
    right_record_id: UUID


class MPIMatchingWorkflow(BaseWorkflow):
    """Orchestrate explainable MPI candidate matching."""

    workflow_name = "patient_mpi.match"

    def __init__(
        self,
        *,
        request: MPIMatchingRequest,
        policy: MPIPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the matching workflow."""

        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MPIPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Generate a candidate and publish its event."""

        actor = User.objects.get(pk=context.actor_id)
        organization = Organization.objects.get(
            pk=self._request.organization_id,
            tenant_id=context.tenant_id,
        )
        if not self._policy.can_match(actor=actor, organization=organization):
            raise PermissionError(
                "You do not have permission to generate MPI matches.",
            )

        records = MPIRecord.objects.filter(
            organization_id=organization.pk,
            organization__tenant_id=context.tenant_id,
            pk__in=(
                self._request.left_record_id,
                self._request.right_record_id,
            ),
        )
        records_by_id = {record.pk: record for record in records}
        if set(records_by_id) != {
            self._request.left_record_id,
            self._request.right_record_id,
        }:
            raise ValueError(
                "Both MPI records must exist in the selected organization and tenant.",
            )

        left = records_by_id[self._request.left_record_id]
        right = records_by_id[self._request.right_record_id]

        candidate = MPIService.create_candidate(
            organization=organization,
            left_record=left,
            right_record=right,
            performed_by=actor,
        )

        self.publish_after_commit(
            MPIMatchCreatedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                organization_id=organization.pk,
                candidate_id=candidate.pk,
                left_record_id=candidate.left_record_id,
                right_record_id=candidate.right_record_id,
            ),
        )

        return WorkflowResult.ok(
            context=context,
            data=candidate,
            message="MPI candidate match generated successfully.",
            code="patient_mpi_match_created",
        )


__all__ = (
    "MPIMatchingRequest",
    "MPIMatchingWorkflow",
)
