"""Patient Communication creation workflow."""

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
from apps.patient_management.communication.events.created import (
    CommunicationCreatedEvent,
)
from apps.patient_management.communication.policies.communication import (
    PatientCommunicationPolicy,
)
from apps.patient_management.communication.services.communication import (
    PatientCommunicationService,
)


@dataclass(frozen=True)
class CommunicationCreationData:
    """Workflow output data."""

    communication: Any


@dataclass(frozen=True)
class CommunicationCreationRequest:
    """Workflow input data."""

    tenant_id: UUID
    organization: Any
    validated_data: dict[str, Any] = field(default_factory=dict)
    actor: Any = None


class CommunicationCreationWorkflow(BaseWorkflow):
    """Create Patient Communication through policy and service layers."""

    name = "patient_communication.create"

    def __init__(
        self, *, request: CommunicationCreationRequest, logger_: Any = None
    ) -> None:
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute the creation transaction."""
        request = self.request
        if not PatientCommunicationPolicy.can_create(
            actor=request.actor, organization=request.organization
        ):
            raise PermissionError(
                "Insufficient permission to create Patient Communication."
            )
        communication = PatientCommunicationService.create(
            validated_data=request.validated_data,
            performed_by=request.actor,
        )
        event = CommunicationCreatedEvent(
            communication=communication,
            actor_id=getattr(request.actor, "id", request.actor),
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(data={"communication_created": communication})


workflow_registry.register(
    name="patient_communication.create", workflow=CommunicationCreationWorkflow
)

__all__ = (
    "CommunicationCreationData",
    "CommunicationCreationRequest",
    "CommunicationCreationWorkflow",
)
