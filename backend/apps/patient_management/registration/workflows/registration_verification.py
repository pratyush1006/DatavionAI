"""
Patient Registration verification workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows.base import BaseWorkflow
from apps.core.workflows.context import WorkflowContext
from apps.core.workflows.result import WorkflowResult
from apps.patient_management.registration.events.registration_verified import (
    RegistrationVerifiedEvent,
)
from apps.patient_management.registration.models.registration import (
    PatientRegistration,
)
from apps.patient_management.registration.policies.registration import (
    RegistrationPolicy,
)
from apps.patient_management.registration.services.registration import (
    PatientRegistrationService,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationVerificationRequest:
    """
    Input contract for verifying a patient registration.
    """

    organization_id: UUID
    registration_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationVerificationData:
    """
    Result data returned by the Registration verification workflow.
    """

    registration_id: UUID
    verified: bool
    verified_at: datetime | None
    event_id: UUID | None = None


class RegistrationVerificationWorkflow(
    BaseWorkflow[RegistrationVerificationData],
):
    """
    Orchestrates authorization and domain mutation for Registration
    verification.

    The workflow owns actor resolution, tenant scoping, authorization,
    service invocation, and domain-event publication.
    """

    workflow_name = "registration.verify"

    def __init__(
        self,
        *,
        request: RegistrationVerificationRequest,
        policy: RegistrationPolicy | None = None,
    ) -> None:
        super().__init__()
        self._request = request
        self._policy = policy or RegistrationPolicy()

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[RegistrationVerificationData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )

            registration = PatientRegistration.objects.select_related(
                "organization",
                "patient",
                "verified_by",
            ).get(
                id=self._request.registration_id,
                organization_id=organization.pk,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested organization or registration was not found."
            ) from exc

        if not self._policy.can_verify(
            actor=actor,
            registration=registration,
        ):
            raise PermissionError(
                "You do not have permission to verify this patient registration."
            )

        verified_registration = PatientRegistrationService.verify(
            instance=registration,
            performed_by=actor,
        )

        event = RegistrationVerifiedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            registration_id=verified_registration.id,
            patient_id=verified_registration.patient_id,
            organization_id=verified_registration.organization_id,
            registration_number=verified_registration.registration_number,
            verification_method=verified_registration.verification_method,
            verified_at=(
                verified_registration.verified_at.isoformat()
                if verified_registration.verified_at
                else None
            ),
            registration_status=verified_registration.registration_status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=RegistrationVerificationData(
                registration_id=verified_registration.id,
                verified=verified_registration.verified,
                verified_at=verified_registration.verified_at,
                event_id=event.event_id,
            ),
        )


__all__ = (
    "RegistrationVerificationData",
    "RegistrationVerificationRequest",
    "RegistrationVerificationWorkflow",
)
