"""
Patient Referral lifecycle workflow.
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
from apps.patient_management.referrals.events import ReferralStatusChangedEvent
from apps.patient_management.referrals.exceptions import (
    ReferralError,
    referral_failure_result,
)
from apps.patient_management.referrals.models import PatientReferral
from apps.patient_management.referrals.policies import PatientReferralPolicy
from apps.patient_management.referrals.services import PatientReferralService
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ReferralLifecycleRequest:
    """Input required for a referral lifecycle transition."""

    organization_id: UUID
    referral_id: UUID
    target_status: str


class ReferralLifecycleWorkflow(BaseWorkflow):
    """Orchestrate strict Patient Referral lifecycle transitions."""

    workflow_name = "patient_referral.lifecycle"

    def __init__(
        self,
        *,
        request: ReferralLifecycleRequest,
        policy: PatientReferralPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the lifecycle workflow."""

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
        """Transition the referral and publish its event after commit."""

        try:
            actor = User.objects.get(pk=context.actor_id)
            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
            referral = (
                PatientReferral.objects.select_for_update()
                .select_related("organization", "patient")
                .get(
                    pk=self._request.referral_id,
                    organization_id=organization.pk,
                    organization__tenant_id=context.tenant_id,
                )
            )

            if not self._policy.can_transition(
                user=actor,
                referral=referral,
            ):
                raise PermissionError(
                    "You do not have permission to transition patient referrals.",
                )

            previous_status = referral.status
            referral = PatientReferralService.transition(
                referral=referral,
                target_status=self._request.target_status,
                performed_by=actor,
            )
        except (
            ObjectDoesNotExist,
            PermissionError,
            ReferralError,
        ) as exc:
            return referral_failure_result(
                context=context,
                exception=exc,
            )

        event = ReferralStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            referral_id=referral.id,
            patient_id=referral.patient_id,
            organization_id=referral.organization_id,
            previous_status=previous_status,
            status=referral.status,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=referral,
            message="Patient referral status updated successfully.",
            code="patient_referral_status_changed",
        )


__all__ = (
    "ReferralLifecycleRequest",
    "ReferralLifecycleWorkflow",
)
