"""
Patient Timeline restore workflow.
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
from apps.patient_management.timeline.events import TimelineRestoredEvent
from apps.patient_management.timeline.policies import TimelinePolicy
from apps.patient_management.timeline.selectors import get_timeline
from apps.patient_management.timeline.services import restore_timeline
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TimelineRestoreRequest:
    """Input required to restore a deleted Timeline entry."""

    timeline_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TimelineRestoreData:
    """Result data returned by Timeline restoration."""

    timeline_id: UUID
    patient_id: UUID
    organization_id: UUID
    restored: bool
    event_id: UUID | None = None


class TimelineRestoreWorkflow(
    BaseWorkflow[TimelineRestoreData],
):
    """Orchestrate restoration of deleted Timeline entries."""

    workflow_name = "timeline.restore"

    def __init__(
        self,
        *,
        request: TimelineRestoreRequest,
        policy: TimelinePolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the restore workflow."""

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
    ) -> WorkflowResult[TimelineRestoreData]:
        """Restore a deleted Timeline entry and publish its event after commit."""

        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            timeline = get_timeline(
                tenant_id=context.tenant_id,
                timeline_id=self._request.timeline_id,
                include_deleted=True,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested timeline entry was not found.",
            ) from exc

        if not timeline.is_deleted:
            raise ValueError(
                "The requested timeline entry is not deleted.",
            )

        if not self._policy.can_restore(
            actor=actor,
            entry=timeline,
        ):
            raise PermissionError(
                "You do not have permission to restore patient timeline entries.",
            )

        timeline = restore_timeline(
            instance=timeline,
            performed_by=actor,
        )

        event = TimelineRestoredEvent(
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
            data=TimelineRestoreData(
                timeline_id=timeline.id,
                patient_id=timeline.patient_id,
                organization_id=timeline.organization_id,
                restored=True,
                event_id=event.event_id,
            ),
            message="Patient timeline entry restored successfully.",
            code="timeline_restored",
        )


__all__ = (
    "TimelineRestoreData",
    "TimelineRestoreRequest",
    "TimelineRestoreWorkflow",
)
