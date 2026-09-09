"""
Patient Timeline deletion workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.timeline.events import TimelineDeletedEvent
from apps.patient_management.timeline.policies import TimelinePolicy
from apps.patient_management.timeline.selectors import get_timeline
from apps.patient_management.timeline.services import delete_timeline
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TimelineDeletionRequest:
    """Input required to delete a Timeline entry."""

    timeline_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TimelineDeletionData:
    """Result data returned by Timeline deletion."""

    timeline_id: UUID
    patient_id: UUID
    organization_id: UUID
    deleted: bool
    event_id: UUID | None = None


class TimelineDeletionWorkflow(
    BaseWorkflow[TimelineDeletionData],
):
    """Orchestrate Timeline deletion."""

    workflow_name = "timeline.delete"

    def __init__(
        self,
        *,
        request: TimelineDeletionRequest,
        policy: TimelinePolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the deletion workflow."""

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
    ) -> WorkflowResult[TimelineDeletionData]:
        """Delete a Timeline entry and publish its event after commit."""

        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            timeline = get_timeline(
                tenant_id=context.tenant_id,
                timeline_id=self._request.timeline_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested timeline entry was not found.",
            ) from exc

        if not self._policy.can_delete(
            actor=actor,
            entry=timeline,
        ):
            raise PermissionError(
                "You do not have permission to delete patient timeline entries.",
            )

        delete_timeline(
            instance=timeline,
            performed_by=actor,
        )

        event = TimelineDeletedEvent(
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
            data=TimelineDeletionData(
                timeline_id=timeline.id,
                patient_id=timeline.patient_id,
                organization_id=timeline.organization_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Patient timeline entry deleted successfully.",
            code="timeline_deleted",
        )


__all__ = (
    "TimelineDeletionData",
    "TimelineDeletionRequest",
    "TimelineDeletionWorkflow",
)
