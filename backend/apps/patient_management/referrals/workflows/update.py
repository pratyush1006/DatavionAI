"""
Patient Referral update workflow.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.referrals.events import ReferralUpdatedEvent
from apps.patient_management.referrals.exceptions import (
    ReferralError,
    referral_failure_result,
)
from apps.patient_management.referrals.policies import PatientReferralPolicy
from apps.patient_management.referrals.selectors import get_referral
from apps.patient_management.referrals.services import PatientReferralService
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ReferralUpdateRequest:
    """Input required to update a referral."""

    organization_id: UUID
    referral_id: UUID
    data: Mapping[str, object]


class ReferralUpdateWorkflow(BaseWorkflow):
    """Orchestrate organization-scoped referral updates."""

    workflow_name = "patient_referral.update"

    def __init__(
        self,
        *,
        request: ReferralUpdateRequest,
        policy: PatientReferralPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the referral update workflow."""

        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientReferralPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """Update the referral and publish its event after commit."""

        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
            referral = get_referral(
                referral_id=self._request.referral_id,
                tenant_id=context.tenant_id,
                organization_id=organization.pk,
            )

            if not self._policy.can_update(
                user=actor,
                referral=referral,
            ):
                raise PermissionError(
                    "You do not have permission to update patient referrals.",
                )

            referral = PatientReferralService.update(
                referral=referral,
                performed_by=actor,
                **dict(self._request.data),
            )
        except (
            ObjectDoesNotExist,
            PermissionError,
            ReferralError,
            IntegrityError,
        ) as exc:
            return referral_failure_result(
                context=context,
                exception=exc,
            )

        event = ReferralUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            referral_id=referral.id,
            patient_id=referral.patient_id,
            organization_id=referral.organization_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=referral,
            message="Patient referral updated successfully.",
            code="patient_referral_updated",
        )


__all__ = (
    "ReferralUpdateRequest",
    "ReferralUpdateWorkflow",
)
