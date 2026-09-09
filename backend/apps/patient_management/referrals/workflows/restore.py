"""
Patient Referral restoration workflow.
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
from apps.patient_management.referrals.events import ReferralRestoredEvent
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
class ReferralRestoreRequest:
    """Input required to restore a referral."""

    organization_id: UUID
    referral_id: UUID


class ReferralRestoreWorkflow(BaseWorkflow):
    """Orchestrate restoration of a deleted Patient Referral."""

    workflow_name = "patient_referral.restore"

    def __init__(
        self,
        *,
        request: ReferralRestoreRequest,
        policy: PatientReferralPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the restoration workflow."""

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
        """Restore the referral and publish its event after commit."""

        try:
            actor = User.objects.get(pk=context.actor_id)
            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
            referral = (
                PatientReferral.all_objects.select_for_update()
                .select_related("organization", "patient")
                .get(
                    pk=self._request.referral_id,
                    organization_id=organization.pk,
                    organization__tenant_id=context.tenant_id,
                    is_deleted=True,
                )
            )

            if not self._policy.can_restore(
                user=actor,
                referral=referral,
            ):
                raise PermissionError(
                    "You do not have permission to restore patient referrals.",
                )

            referral = PatientReferralService.restore(
                referral=referral,
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

        event = ReferralRestoredEvent(
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
            message="Patient referral restored successfully.",
            code="patient_referral_restored",
        )


__all__ = (
    "ReferralRestoreRequest",
    "ReferralRestoreWorkflow",
)
