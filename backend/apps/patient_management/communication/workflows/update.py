"""Patient Communication update workflow."""

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
from apps.patient_management.communication.events.updated import (
    CommunicationUpdatedEvent,
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
class CommunicationUpdateData:
    """Workflow output data."""

    communication: Any


@dataclass(frozen=True)
class CommunicationUpdateRequest:
    """Workflow input data."""

    tenant_id: UUID
    communication_id: UUID | None = None
    organization: Any = None
    validated_data: dict[str, Any] = field(default_factory=dict)
    actor: Any = None


class CommunicationUpdateWorkflow(BaseWorkflow):
    """Orchestrate Patient Communication update through policy and service layers."""

    name = "patient_communication.update"

    def __init__(
        self, *, request: CommunicationUpdateRequest, logger_: Any = None
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
            include_deleted=False,
        )
        organization = communication.organization
        if not PatientCommunicationPolicy.can_update(
            actor=actor, organization=organization
        ):
            raise PermissionError(
                "Insufficient permission for Patient Communication update."
            )
        if "update" == "update":
            communication = PatientCommunicationService.update(
                instance=communication,
                validated_data=request.validated_data,
                performed_by=actor,
            )
        else:
            communication = PatientCommunicationService.update(
                instance=communication,
                performed_by=actor,
            )
        event = CommunicationUpdatedEvent(
            communication=communication, actor_id=getattr(actor, "id", actor)
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(data={"communication_updated": communication})


workflow_registry.register(
    name="patient_communication.update", workflow=CommunicationUpdateWorkflow
)

__all__ = (
    "CommunicationUpdateData",
    "CommunicationUpdateRequest",
    "CommunicationUpdateWorkflow",
)
