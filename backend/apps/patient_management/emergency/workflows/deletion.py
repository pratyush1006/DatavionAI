"""Workflow for deleting patient emergency contacts."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.emergency.events.deleted import (
    EmergencyContactDeleted,
)
from apps.patient_management.emergency.selectors import EmergencySelector
from apps.patient_management.emergency.services import EmergencyService


@dataclass(frozen=True)
class EmergencyDeletionRequest:
    """Input contract for emergency contact deletion."""

    organization: object
    emergency_id: UUID
    actor: object


class EmergencyDeletionWorkflow(BaseWorkflow):
    """Orchestrate soft deletion of emergency contacts."""

    def __init__(self, *, request: EmergencyDeletionRequest, logger_=None):
        """Initialize the emergency deletion workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Soft-delete an emergency contact and publish its event."""

        request = self.payload
        record = EmergencySelector.get(
            organization=request.organization,
            emergency_id=request.emergency_id,
        )
        record = EmergencyService.delete(record=record)
        self.publish_after_commit(
            EmergencyContactDeleted(
                emergency_id=record.id,
                organization_id=request.organization.id,
                patient_id=record.patient_id,
            ),
        )

        return WorkflowResult.ok(record)


__all__ = (
    "EmergencyDeletionRequest",
    "EmergencyDeletionWorkflow",
)
