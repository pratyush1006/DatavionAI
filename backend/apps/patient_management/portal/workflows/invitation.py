"""
Patient Portal invitation workflow.
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
from apps.patient_management.portal.events import (
    PatientPortalAccountInvitationSentEvent,
)
from apps.patient_management.portal.policies import PatientPortalPolicy
from apps.patient_management.portal.selectors import get_portal_account
from apps.patient_management.portal.services import PatientPortalAccountService
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPortalInvitationRequest:
    """Input required to issue a portal invitation."""

    organization_id: UUID
    account_id: UUID


class PatientPortalInvitationWorkflow(BaseWorkflow):
    """Authorize and issue a portal invitation."""

    workflow_name = "patient_portal.invite"

    def __init__(
        self,
        *,
        request: PatientPortalInvitationRequest,
        policy: PatientPortalPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the invitation workflow."""

        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or PatientPortalPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Issue the invitation and publish its domain event after commit."""

        try:
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
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Organization, portal account, or actor was not found.",
            ) from exc

        if not self._policy.can_invite(actor=actor, account=account):
            raise PermissionError(
                "You do not have permission to issue portal invitations.",
            )

        account = PatientPortalAccountService.mark_invitation_sent(
            account=account,
        )

        event = PatientPortalAccountInvitationSentEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            account_id=account.pk,
            patient_id=account.patient_id,
            organization_id=account.organization_id,
            email=account.email,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=account,
            message="Patient portal invitation issued successfully.",
            code="patient_portal_invitation_sent",
        )


__all__ = (
    "PatientPortalInvitationRequest",
    "PatientPortalInvitationWorkflow",
)
