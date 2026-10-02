"""Patient Communication restore workflow."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
    workflow_registry,
)
from apps.patient_management.communication.events.restored import (
    CommunicationRestoredEvent,
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
class CommunicationRestoreData:
    """Workflow output data."""

    communication: Any


@dataclass(frozen=True)
class CommunicationRestoreRequest:
    """Workflow input data."""

    tenant_id: UUID
    communication_id: UUID | None = None
    organization: Any = None
    validated_data: dict[str, Any] = field(default_factory=dict)
    actor: Any = None


class CommunicationRestoreWorkflow(BaseWorkflow):
    """Orchestrate Patient Communication restore through policy and service layers."""

    name = "patient_communication.restore"

    def __init__(
        self, *, request: CommunicationRestoreRequest, logger_: Any = None
    ) -> None:
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute the workflow transaction."""
        request = self.request
        actor = request.actor
        if request.communication_id is None:
            raise ValueError("communication_id is required")
        communication = get_communication(
            tenant_id=request.tenant_id,
            communication_id=request.communication_id,
            include_deleted=True,
        )
        organization = communication.organization
        if not PatientCommunicationPolicy.can_restore(
            actor=actor, organization=organization
        ):
            raise PermissionError(
                "Insufficient permission for Patient Communication restore."
            )
        if "restore" == "update":
            communication = PatientCommunicationService.restore(
                instance=communication,
                validated_data=request.validated_data,
                performed_by=actor,
            )
        else:
            communication = PatientCommunicationService.restore(
                instance=communication,
                performed_by=actor,
            )
        event = CommunicationRestoredEvent(
            communication=communication, actor_id=getattr(actor, "id", actor)
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(data={"communication_restored": communication})


workflow_registry.register(
    name="patient_communication.restore", workflow=CommunicationRestoreWorkflow
)

__all__ = (
    "CommunicationRestoreData",
    "CommunicationRestoreRequest",
    "CommunicationRestoreWorkflow",
)
