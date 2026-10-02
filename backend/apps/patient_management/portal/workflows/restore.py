"""
Patient Portal restore workflow
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
from apps.patient_management.portal.events import PatientPortalAccountRestoredEvent
from apps.patient_management.portal.models import PatientPortalAccount
from apps.patient_management.portal.policies import PatientPortalPolicy
from apps.patient_management.portal.services import PatientPortalAccountService
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPortalRestoreRequest:
    """Input required to restore a portal account."""

    organization_id: UUID
    account_id: UUID


class PatientPortalRestoreWorkflow(BaseWorkflow):
    """Orchestrate restoration of a deleted portal account."""

    workflow_name = "patient_portal.restore"

    def __init__(
        self,
        *,
        request: PatientPortalRestoreRequest,
        policy: PatientPortalPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the restore workflow."""

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
        """Restore the account and publish its domain event."""

        actor = User.objects.get(pk=context.actor_id)
        organization = Organization.objects.get(
            pk=self._request.organization_id,
            tenant_id=context.tenant_id,
        )
        account = PatientPortalAccount.all_objects.select_related(
            "organization",
            "patient",
        ).get(
            pk=self._request.account_id,
            organization_id=organization.pk,
            organization__tenant_id=context.tenant_id,
            is_deleted=True,
        )

        if not self._policy.can_restore(
            actor=actor,
            account=account,
        ):
            raise PermissionError(
                "You do not have permission to restore portal accounts.",
            )

        PatientPortalAccountService.restore(
            account=account,
            performed_by=actor,
        )

        event = PatientPortalAccountRestoredEvent(
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
            message="Patient portal account restored successfully.",
            code="patient_portal_restored",
        )


__all__ = (
    "PatientPortalRestoreRequest",
    "PatientPortalRestoreWorkflow",
)
