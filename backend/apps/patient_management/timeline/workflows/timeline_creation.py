"""
Patient Timeline creation workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.patients.models import Patient
from apps.patient_management.timeline.events import TimelineCreatedEvent
from apps.patient_management.timeline.policies import TimelinePolicy
from apps.patient_management.timeline.services import create_timeline
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TimelineCreationRequest:
    """Input required to create a Timeline entry."""

    organization_id: UUID
    patient_id: UUID
    data: dict[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TimelineCreationData:
    """Result data returned by Timeline creation."""

    timeline_id: UUID
    patient_id: UUID
    organization_id: UUID
    created: bool
    event_id: UUID | None = None


class TimelineCreationWorkflow(
    BaseWorkflow[TimelineCreationData],
):
    """Orchestrate Timeline creation."""

    workflow_name = "timeline.create"

    def __init__(
        self,
        *,
        request: TimelineCreationRequest,
        policy: TimelinePolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the creation workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or TimelinePolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[TimelineCreationData]:
        """Create a Timeline entry and publish its event after commit."""

        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
            patient = Patient.objects.get(
                pk=self._request.patient_id,
                organization_id=organization.pk,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested organization or patient was not found.",
            ) from exc

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "You do not have permission to create patient timeline entries.",
            )

        data = dict(
            self._request.data,
        )
        data["organization"] = organization
        data["patient"] = patient

        timeline = create_timeline(
            validated_data=data,
            performed_by=actor,
        )

        event = TimelineCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            timeline_id=timeline.id,
            patient_id=timeline.patient_id,
            organization_id=timeline.organization_id,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=TimelineCreationData(
                timeline_id=timeline.id,
                created=True,
                patient_id=timeline.patient_id,
                organization_id=timeline.organization_id,
                event_id=event.event_id,
            ),
            message="Patient timeline entry created successfully.",
            code="timeline_created",
        )


__all__ = (
    "TimelineCreationData",
    "TimelineCreationRequest",
    "TimelineCreationWorkflow",
)
