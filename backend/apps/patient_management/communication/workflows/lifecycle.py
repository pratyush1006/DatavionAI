"""Patient Communication lifecycle workflow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
    workflow_registry,
)
from apps.patient_management.communication.events.status_changed import (
    CommunicationStatusChangedEvent,
)
from apps.patient_management.communication.policies.communication import (
    PatientCommunicationPolicy,
)
from apps.patient_management.communication.selectors.communication import (
    get_communication,
)
from apps.patient_management.communication.services.communication import (
    PatientCommunicationService,
)


@dataclass(frozen=True)
class CommunicationLifecycleData:
    """Workflow output data."""

    communication: Any


@dataclass(frozen=True)
class CommunicationLifecycleRequest:
    """Workflow input data."""

    tenant_id: UUID
    communication_id: UUID
    status: str
    actor: Any = None


class CommunicationLifecycleWorkflow(BaseWorkflow):
    """Apply an authorized communication status transition."""

    name = "patient_communication.lifecycle"

    def __init__(
        self, *, request: CommunicationLifecycleRequest, logger_: Any = None
    ) -> None:
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute the lifecycle transaction."""
        request = self.request
        communication = get_communication(
            tenant_id=request.tenant_id, communication_id=request.communication_id
        )
        if not PatientCommunicationPolicy.can_status(
            actor=request.actor,
            organization=communication.organization,
            status=request.status,
        ):
            raise PermissionError(
                "Insufficient permission for Patient Communication lifecycle transition."
            )
        old_status = communication.status
        communication = PatientCommunicationService.transition(
            instance=communication, status=request.status, performed_by=request.actor
        )
        event = CommunicationStatusChangedEvent(
            communication=communication,
            actor_id=getattr(request.actor, "id", request.actor),
            payload={"old_status": old_status, "new_status": communication.status},
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(data={"communication_status_changed": communication})


workflow_registry.register(
    name="patient_communication.lifecycle", workflow=CommunicationLifecycleWorkflow
)

__all__ = (
    "CommunicationLifecycleData",
    "CommunicationLifecycleRequest",
    "CommunicationLifecycleWorkflow",
)
