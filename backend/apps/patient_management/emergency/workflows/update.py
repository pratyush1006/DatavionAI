"""Workflow for updating patient emergency contacts."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.emergency.events.updated import (
    EmergencyContactUpdated,
)
from apps.patient_management.emergency.selectors import EmergencySelector
from apps.patient_management.emergency.services import EmergencyService


@dataclass(frozen=True)
class EmergencyUpdateRequest:
    """Input contract for emergency contact updates."""

    organization: object
    emergency_id: UUID
    data: dict
    actor: object


class EmergencyUpdateWorkflow(BaseWorkflow):
    """Orchestrate emergency contact updates."""

    def __init__(self, *, request: EmergencyUpdateRequest, logger_=None):
        """Initialize the emergency update workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Update an emergency contact and publish its event."""

        request = self.payload
        record = EmergencySelector.get(
            organization=request.organization,
            emergency_id=request.emergency_id,
        )
        record = EmergencyService.update(
            record=record,
            data=request.data,
        )
        self.publish_after_commit(
            EmergencyContactUpdated(
                emergency_id=record.id,
                organization_id=request.organization.id,
                patient_id=record.patient_id,
            ),
        )

        return WorkflowResult.ok(record)


__all__ = (
    "EmergencyUpdateRequest",
    "EmergencyUpdateWorkflow",
)
