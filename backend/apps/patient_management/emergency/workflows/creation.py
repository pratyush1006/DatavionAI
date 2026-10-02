"""Workflow for creating patient emergency contacts."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.emergency.events.created import (
    EmergencyContactCreated,
)
from apps.patient_management.emergency.services import EmergencyService
from apps.patient_management.patients.models import Patient


@dataclass(frozen=True)
class EmergencyCreationRequest:
    """Input contract for emergency contact creation."""

    organization: object
    patient_id: UUID
    data: dict
    actor: object


class EmergencyCreationWorkflow(BaseWorkflow):
    """Orchestrate authorization-safe emergency contact creation."""

    def __init__(self, *, request: EmergencyCreationRequest, logger_=None):
        """Initialize the emergency creation workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Create an emergency contact and publish its domain event."""

        request = self.payload
        patient = Patient.objects.get(
            id=request.patient_id,
            organization=request.organization,
        )
        record = EmergencyService.create(
            organization=request.organization,
            patient=patient,
            data=request.data,
        )
        self.publish_after_commit(
            EmergencyContactCreated(
                emergency_id=record.id,
                organization_id=request.organization.id,
                patient_id=patient.id,
            ),
        )

        return WorkflowResult.ok(record)


__all__ = (
    "EmergencyCreationRequest",
    "EmergencyCreationWorkflow",
)
