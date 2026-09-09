"""Workflow for patient emergency lifecycle operations."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.emergency.constants import (
    EmergencyRecordStatus,
)
from apps.patient_management.emergency.events.status_changed import (
    EmergencyContactStatusChanged,
)
from apps.patient_management.emergency.selectors import EmergencySelector
from apps.patient_management.emergency.services import EmergencyService


@dataclass(frozen=True)
class EmergencyLifecycleRequest:
    """Input contract for emergency lifecycle operations."""

    organization: object
    emergency_id: UUID
    action: str
    actor: object


class EmergencyLifecycleWorkflow(BaseWorkflow):
    """Orchestrate activation and deactivation operations."""

    def __init__(self, *, request: EmergencyLifecycleRequest, logger_=None):
        """Initialize the emergency lifecycle workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute a lifecycle transition and publish its event."""

        request = self.payload
        record = EmergencySelector.get(
            organization=request.organization,
            emergency_id=request.emergency_id,
        )

        if request.action == EmergencyRecordStatus.ACTIVE:
            record = EmergencyService.activate(record=record)
        elif request.action == EmergencyRecordStatus.INACTIVE:
            record = EmergencyService.deactivate(record=record)
        else:
            raise ValueError(
                f"Unsupported emergency lifecycle action: {request.action}",
            )

        self.publish_after_commit(
            EmergencyContactStatusChanged(
                emergency_id=record.id,
                organization_id=request.organization.id,
                patient_id=record.patient_id,
            ),
        )

        return WorkflowResult.ok(record)


__all__ = (
    "EmergencyLifecycleRequest",
    "EmergencyLifecycleWorkflow",
)
