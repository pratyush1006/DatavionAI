"""
Patient Registration cancellation workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows.base import BaseWorkflow
from apps.core.workflows.context import WorkflowContext
from apps.core.workflows.result import WorkflowResult
from apps.patient_management.registration.events.registration_cancelled import (
    RegistrationCancelledEvent,
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
class RegistrationCancellationRequest:
    """
    Input contract for cancelling a patient registration.
    """

    organization_id: UUID
    registration_id: UUID
    reason: str
    notes: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationCancellationData:
    """
    Result data returned by the Registration cancellation workflow.
    """

    registration_id: UUID
    cancelled: bool
    event_id: UUID | None = None


class RegistrationCancellationWorkflow(
    BaseWorkflow[RegistrationCancellationData],
):
    """
    Orchestrates authorization and domain mutation for Registration
    cancellation.

    The workflow owns:
    - actor resolution
    - tenant scoping
    - organization scoping
    - authorization
    - service invocation
    - domain-event publication
    """

    workflow_name = "registration.cancel"

    def __init__(
        self,
        *,
        request: RegistrationCancellationRequest,
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
    ) -> WorkflowResult[RegistrationCancellationData]:
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
                uuid=self._request.registration_id,
                organization_id=organization.pk,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested organization or registration was not found.",
            ) from exc

        if not self._policy.can_cancel(
            actor=actor,
            organization=organization,
            registration=registration,
        ):
            raise PermissionError(
                "You do not have permission to cancel this patient registration.",
            )

        cancelled_registration = PatientRegistrationService.cancel(
            instance=registration,
            reason=self._request.reason,
            notes=self._request.notes,
            performed_by=actor,
        )

        event = RegistrationCancelledEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            registration_id=cancelled_registration.uuid,
            patient_id=cancelled_registration.patient_id,
            organization_id=cancelled_registration.organization_id,
            registration_number=cancelled_registration.registration_number,
            cancellation_reason=cancelled_registration.cancellation_reason,
            registration_status=cancelled_registration.registration_status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=RegistrationCancellationData(
                registration_id=cancelled_registration.uuid,
                cancelled=cancelled_registration.is_cancelled,
                event_id=event.event_id,
            ),
            message="Patient registration cancelled successfully.",
            code="registration_cancelled",
        )


__all__ = (
    "RegistrationCancellationData",
    "RegistrationCancellationRequest",
    "RegistrationCancellationWorkflow",
)
