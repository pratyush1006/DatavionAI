"""
Patient Timeline lifecycle workflow.
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
from apps.patient_management.timeline.constants import TimelineStatus
from apps.patient_management.timeline.events import TimelineStatusChangedEvent
from apps.patient_management.timeline.policies import TimelinePolicy
from apps.patient_management.timeline.selectors import get_timeline
from apps.patient_management.timeline.services import (
    activate_timeline,
    archive_timeline,
    deactivate_timeline,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TimelineLifecycleRequest:
    """Input required to change Timeline lifecycle status."""

    timeline_id: UUID
    status: str


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TimelineLifecycleData:
    """Result data returned by a lifecycle transition."""

    timeline_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str
    changed: bool
    event_id: UUID | None = None


class TimelineLifecycleWorkflow(
    BaseWorkflow[TimelineLifecycleData],
):
    """Orchestrate Timeline lifecycle transitions."""

    workflow_name = "timeline.lifecycle"

    def __init__(
        self,
        *,
        request: TimelineLifecycleRequest,
        policy: TimelinePolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the lifecycle workflow."""

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
    ) -> WorkflowResult[TimelineLifecycleData]:
        """Apply a lifecycle transition and publish its event."""

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

        previous_status = timeline.status
        requested_status = self._request.status

        if requested_status == TimelineStatus.ACTIVE:
            allowed = self._policy.can_activate(
                actor=actor,
                entry=timeline,
            )
            if not allowed:
                raise PermissionError(
                    "You do not have permission to activate patient timeline entries.",
                )
            timeline = activate_timeline(
                instance=timeline,
                performed_by=actor,
            )
        elif requested_status == TimelineStatus.DRAFT:
            allowed = self._policy.can_deactivate(
                actor=actor,
                entry=timeline,
            )
            if not allowed:
                raise PermissionError(
                    "You do not have permission to deactivate patient timeline entries.",
                )
            timeline = deactivate_timeline(
                instance=timeline,
                performed_by=actor,
            )
        elif requested_status == TimelineStatus.ARCHIVED:
            allowed = self._policy.can_archive(
                actor=actor,
                entry=timeline,
            )
            if not allowed:
                raise PermissionError(
                    "You do not have permission to archive patient timeline entries.",
                )
            timeline = archive_timeline(
                instance=timeline,
                performed_by=actor,
            )
        else:
            raise ValueError(
                "Unsupported Timeline lifecycle status.",
            )

        changed = previous_status != timeline.status

        event = TimelineStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            timeline_id=timeline.id,
            patient_id=timeline.patient_id,
            organization_id=timeline.organization_id,
            previous_status=previous_status,
            new_status=timeline.status,
        )

        if changed:
            self.publish_after_commit(
                event,
            )

        return WorkflowResult.ok(
            context=context,
            data=TimelineLifecycleData(
                timeline_id=timeline.id,
                patient_id=timeline.patient_id,
                organization_id=timeline.organization_id,
                previous_status=previous_status,
                new_status=timeline.status,
                changed=changed,
                event_id=event.event_id if changed else None,
            ),
            message="Patient timeline lifecycle updated successfully.",
            code="timeline_lifecycle_updated",
        )


__all__ = (
    "TimelineLifecycleData",
    "TimelineLifecycleRequest",
    "TimelineLifecycleWorkflow",
)
