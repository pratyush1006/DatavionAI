"""
Patient Portal update workflow
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.portal.events import PatientPortalAccountUpdatedEvent
from apps.patient_management.portal.policies import PatientPortalPolicy
from apps.patient_management.portal.selectors import get_portal_account
from apps.patient_management.portal.services import PatientPortalAccountService
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPortalUpdateRequest:
    """Input required to update a portal account."""

    organization_id: UUID
    account_id: UUID
    data: dict


class PatientPortalUpdateWorkflow(BaseWorkflow):
    """Orchestrate portal account updates."""

    workflow_name = "patient_portal.update"

    def __init__(
        self,
        *,
        request: PatientPortalUpdateRequest,
        policy: PatientPortalPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the update workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientPortalPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """Update the account and publish its domain event."""

        actor = User.objects.get(pk=context.actor_id)
        organization = Organization.objects.get(
            pk=self._request.organization_id,
            tenant_id=context.tenant_id,
        )
        account = get_portal_account(
            tenant_id=context.tenant_id,
            organization_id=organization.pk,
            account_id=self._request.account_id,
        )

        if not self._policy.can_update(
            actor=actor,
            account=account,
        ):
            raise PermissionError(
                "You do not have permission to update portal accounts.",
            )

        changes = dict(self._request.data)

        account = PatientPortalAccountService.update(
            account=account,
            data=changes,
            performed_by=actor,
        )

        event = PatientPortalAccountUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            account_id=account.pk,
            patient_id=account.patient_id,
            organization_id=account.organization_id,
            changes=changes,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=account,
            message="Patient portal account updated successfully.",
            code="patient_portal_updated",
        )


__all__ = (
    "PatientPortalUpdateRequest",
    "PatientPortalUpdateWorkflow",
)
