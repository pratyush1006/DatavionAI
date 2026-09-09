"""
Patient Timeline update workflow.
"""

from __future__ import annotations

from collections.abc import Mapping
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
from apps.patient_management.timeline.events import TimelineUpdatedEvent
from apps.patient_management.timeline.policies import TimelinePolicy
from apps.patient_management.timeline.selectors import get_timeline
from apps.patient_management.timeline.services import update_timeline
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TimelineUpdateRequest:
    """Input required to update a Timeline entry."""

    timeline_id: UUID
    data: Mapping[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TimelineUpdateData:
    """Result data returned by Timeline update."""

    timeline_id: UUID
    patient_id: UUID
    organization_id: UUID
    updated: bool
    event_id: UUID | None = None


class TimelineUpdateWorkflow(
    BaseWorkflow[TimelineUpdateData],
):
    """Orchestrate Timeline updates."""

    workflow_name = "timeline.update"

    def __init__(
        self,
        *,
        request: TimelineUpdateRequest,
        policy: TimelinePolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the update workflow."""

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
    ) -> WorkflowResult[TimelineUpdateData]:
        """Update a Timeline entry and publish its event after commit."""

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

        if not self._policy.can_update(
            actor=actor,
            entry=timeline,
        ):
            raise PermissionError(
                "You do not have permission to update patient timeline entries.",
            )

        timeline = update_timeline(
            instance=timeline,
            validated_data=dict(
                self._request.data,
            ),
        )

        event = TimelineUpdatedEvent(
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
            data=TimelineUpdateData(
                timeline_id=timeline.id,
                patient_id=timeline.patient_id,
                organization_id=timeline.organization_id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient timeline entry updated successfully.",
            code="timeline_updated",
        )


__all__ = (
    "TimelineUpdateData",
    "TimelineUpdateRequest",
    "TimelineUpdateWorkflow",
)
