"""Workflow orchestration for Denials."""

from __future__ import annotations

from dataclasses import dataclass

from apps.core.events import publish_after_commit
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult

from .events import DenialCreatedEvent, DenialStatusChangedEvent
from .services import create_denial, transition_denial


@dataclass(frozen=True)
class CreateDenialRequest:
    """Creation workflow input."""

    organization: object
    patient: object
    actor: object
    data: dict


@dataclass(frozen=True)
class TransitionDenialRequest:
    """Transition workflow input."""

    denial: object
    target_status: str
    actor: object
    resolution_note: str = ""


class DenialCreationWorkflow(BaseWorkflow):
    """Create a denial and publish its event after commit."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute creation."""
        request = context.payload
        denial = create_denial(
            organization=request.organization,
            patient=request.patient,
            actor=request.actor,
            data=request.data,
        )
        publish_after_commit(
            DenialCreatedEvent(
                denial_id=denial.id,
                organization_id=denial.organization_id,
                patient_id=denial.patient_id,
            )
        )
        return WorkflowResult.ok(context=context, data=denial)


class DenialTransitionWorkflow(BaseWorkflow):
    """Transition a denial and publish its event after commit."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute transition."""
        request = context.payload
        previous = request.denial.status
        denial = transition_denial(
            denial=request.denial,
            target_status=request.target_status,
            resolution_note=request.resolution_note,
        )
        publish_after_commit(
            DenialStatusChangedEvent(
                denial_id=denial.id,
                organization_id=denial.organization_id,
                previous_status=previous,
                new_status=denial.status,
            )
        )
        return WorkflowResult.ok(context=context, data=denial)


__all__ = (
    "CreateDenialRequest",
    "TransitionDenialRequest",
    "DenialCreationWorkflow",
    "DenialTransitionWorkflow",
)
