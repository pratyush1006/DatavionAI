"""
Patient Registration check-in workflow.
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
from apps.patient_management.registration.events.registration_checked_in import (
    RegistrationCheckedInEvent,
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
class RegistrationCheckInRequest:
    """
    Input contract for checking in a patient registration.
    """

    organization_id: UUID
    registration_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationCheckInData:
    """
    Result data returned by the Registration check-in workflow.
    """

    registration_id: UUID
    checked_in: bool
    checked_in_at: datetime | None
    event_id: UUID | None = None


class RegistrationCheckInWorkflow(
    BaseWorkflow[RegistrationCheckInData],
):
    """
    Orchestrates authorization and domain mutation for Registration
    check-in.

    The workflow owns actor resolution, tenant scoping, authorization,
    service invocation, and domain-event publication.
    """

    workflow_name = "registration.check_in"

    def __init__(
        self,
        *,
        request: RegistrationCheckInRequest,
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
    ) -> WorkflowResult[RegistrationCheckInData]:
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

        if not self._policy.can_check_in(
            actor=actor,
            registration=registration,
        ):
            raise PermissionError(
                "You do not have permission to check in this patient registration."
            )

        checked_in_registration = PatientRegistrationService.check_in(
            instance=registration,
            performed_by=actor,
        )

        event = RegistrationCheckedInEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            registration_id=checked_in_registration.id,
            patient_id=checked_in_registration.patient_id,
            organization_id=checked_in_registration.organization_id,
            registration_number=checked_in_registration.registration_number,
            checked_in_at=(
                checked_in_registration.checked_in_at.isoformat()
                if checked_in_registration.checked_in_at
                else None
            ),
            registration_status=checked_in_registration.registration_status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=RegistrationCheckInData(
                registration_id=checked_in_registration.id,
                checked_in=True,
                checked_in_at=checked_in_registration.checked_in_at,
                event_id=event.event_id,
            ),
        )


__all__ = (
    "RegistrationCheckInData",
    "RegistrationCheckInRequest",
    "RegistrationCheckInWorkflow",
)
