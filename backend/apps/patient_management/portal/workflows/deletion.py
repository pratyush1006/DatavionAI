"""
Patient Portal deletion workflow
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
from apps.patient_management.portal.events import PatientPortalAccountDeletedEvent
from apps.patient_management.portal.policies import PatientPortalPolicy
from apps.patient_management.portal.selectors import get_portal_account
from apps.patient_management.portal.services import PatientPortalAccountService
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPortalDeletionRequest:
    """Input required to delete a portal account."""

    organization_id: UUID
    account_id: UUID


class PatientPortalDeletionWorkflow(BaseWorkflow):
    """Orchestrate portal account soft deletion."""

    workflow_name = "patient_portal.delete"

    def __init__(
        self,
        *,
        request: PatientPortalDeletionRequest,
        policy: PatientPortalPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the deletion workflow."""

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
        """Delete the account and publish its domain event."""

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

        if not self._policy.can_delete(
            actor=actor,
            account=account,
        ):
            raise PermissionError(
                "You do not have permission to delete portal accounts.",
            )

        PatientPortalAccountService.delete(
            account=account,
            performed_by=actor,
        )

        event = PatientPortalAccountDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            account_id=account.pk,
            patient_id=account.patient_id,
            organization_id=account.organization_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=account,
            message="Patient portal account deleted successfully.",
            code="patient_portal_deleted",
        )


__all__ = (
    "PatientPortalDeletionRequest",
    "PatientPortalDeletionWorkflow",
)
