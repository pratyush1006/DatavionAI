"""
Revenue Cycle Appeals workflow exports.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from django.contrib.auth import get_user_model

from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.revenue_cycle.appeals.services import AppealService


def _actor(context: WorkflowContext):
    return get_user_model().objects.get(pk=context.actor_id)


class AppealCreateWorkflow:
    """Orchestrate appeal creation."""

    def execute(
        self,
        *,
        context: WorkflowContext,
        organization_id: UUID,
        patient_id: UUID,
        data: dict[str, Any],
    ) -> WorkflowResult:
        """Create an appeal through the application service."""
        appeal = AppealService.create(
            actor=_actor(context),
            tenant_id=context.tenant_id,
            organization_id=organization_id,
            patient_id=patient_id,
            data=data,
        )
        return WorkflowResult.ok(
            context=context,
            data=appeal,
        )


class AppealTransitionWorkflow:
    """Orchestrate appeal lifecycle transitions."""

    def execute(
        self,
        *,
        context: WorkflowContext,
        organization_id: UUID,
        appeal_id: UUID,
        target_status: str,
        reason: str = "",
    ) -> WorkflowResult:
        """Transition an appeal through the application service."""
        appeal = AppealService.transition(
            actor=_actor(context),
            tenant_id=context.tenant_id,
            organization_id=organization_id,
            appeal_id=appeal_id,
            target_status=target_status,
            reason=reason,
        )
        return WorkflowResult.ok(
            context=context,
            data=appeal,
        )


class AppealDeletionWorkflow:
    """Orchestrate appeal deletion."""

    def execute(
        self,
        *,
        context: WorkflowContext,
        organization_id: UUID,
        appeal_id: UUID,
    ) -> WorkflowResult:
        """Delete an appeal through the application service."""
        appeal = AppealService.delete(
            actor=_actor(context),
            tenant_id=context.tenant_id,
            organization_id=organization_id,
            appeal_id=appeal_id,
        )
        return WorkflowResult.ok(
            context=context,
            data=appeal,
        )


class AppealRestoreWorkflow:
    """Orchestrate appeal restoration."""

    def execute(
        self,
        *,
        context: WorkflowContext,
        organization_id: UUID,
        appeal_id: UUID,
    ) -> WorkflowResult:
        """Restore an appeal through the application service."""
        appeal = AppealService.restore(
            actor=_actor(context),
            tenant_id=context.tenant_id,
            organization_id=organization_id,
            appeal_id=appeal_id,
        )
        return WorkflowResult.ok(
            context=context,
            data=appeal,
        )


__all__ = (
    "AppealCreateWorkflow",
    "AppealDeletionWorkflow",
    "AppealRestoreWorkflow",
    "AppealTransitionWorkflow",
)
