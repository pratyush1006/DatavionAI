"""
Patient Referral creation workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.patients.models import Patient
from apps.patient_management.referrals.events import ReferralCreatedEvent
from apps.patient_management.referrals.exceptions import (
    referral_failure_result,
)
from apps.patient_management.referrals.policies import PatientReferralPolicy
from apps.patient_management.referrals.services import PatientReferralService
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ReferralCreationRequest:
    """Input required to create a Patient Referral."""

    organization_id: UUID
    patient_id: UUID
    data: dict[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ReferralCreationData:
    """Result data returned by referral creation."""

    referral_id: UUID
    patient_id: UUID
    organization_id: UUID
    created: bool
    event_id: UUID | None = None


class ReferralCreationWorkflow(
    BaseWorkflow[ReferralCreationData],
):
    """Orchestrate tenant-safe Patient Referral creation."""

    workflow_name = "patient_referral.create"

    def __init__(
        self,
        *,
        request: ReferralCreationRequest,
        policy: PatientReferralPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the referral creation workflow."""

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
    ) -> WorkflowResult[ReferralCreationData]:
        """Create a referral and publish its event after commit."""

        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
            patient = Patient.objects.get(
                pk=self._request.patient_id,
                organization_id=organization.pk,
                tenant_id=context.tenant_id,
            )

            if not self._policy.can_create(
                user=actor,
                organization=organization,
            ):
                raise PermissionError(
                    "You do not have permission to create patient referrals.",
                )

            data = dict(self._request.data)
            try:
                referral = PatientReferralService.create(
                    patient=patient,
                    organization=organization,
                    performed_by=actor,
                    **data,
                )
            except IntegrityError as exc:
                raise IntegrityError(
                    "A referral with this referral number already exists "
                    "in the organization.",
                ) from exc

        except (ObjectDoesNotExist, PermissionError, IntegrityError) as exc:
            return referral_failure_result(
                context=context,
                exception=exc,
            )
        except Exception:
            raise

        event = ReferralCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            referral_id=referral.id,
            patient_id=referral.patient_id,
            organization_id=referral.organization_id,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=ReferralCreationData(
                referral_id=referral.id,
                patient_id=referral.patient_id,
                organization_id=referral.organization_id,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient referral created successfully.",
            code="patient_referral_created",
        )


__all__ = (
    "ReferralCreationData",
    "ReferralCreationRequest",
    "ReferralCreationWorkflow",
)
