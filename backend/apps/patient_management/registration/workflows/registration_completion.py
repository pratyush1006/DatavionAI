"""
Patient Registration completion workflow.
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
from apps.patient_management.registration.events.registration_completed import (
    RegistrationCompletedEvent,
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
class RegistrationCompletionRequest:
    """
    Input contract for completing a patient registration.
    """

    organization_id: UUID
    registration_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationCompletionData:
    """
    Result data returned by the Registration completion workflow.
    """

    registration_id: UUID
    completed: bool
    completed_at: datetime | None
    event_id: UUID | None = None


class RegistrationCompletionWorkflow(
    BaseWorkflow[RegistrationCompletionData],
):
    """
    Orchestrates authorization and domain mutation for Registration
    completion.

    The workflow owns actor resolution, tenant scoping, authorization,
    service invocation, and domain-event publication.
    """

    workflow_name = "registration.complete"

    def __init__(
        self,
        *,
        request: RegistrationCompletionRequest,
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
    ) -> WorkflowResult[RegistrationCompletionData]:
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
                "The requested organization or registration was not found."
            ) from exc

        if not self._policy.can_complete(
            actor=actor,
            organization=organization,
            registration=registration,
        ):
            raise PermissionError(
                "You do not have permission to complete this patient registration."
            )

        completed_registration = PatientRegistrationService.complete(
            instance=registration,
            performed_by=actor,
        )

        event = RegistrationCompletedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            registration_id=completed_registration.uuid,
            patient_id=completed_registration.patient_id,
            organization_id=completed_registration.organization_id,
            registration_number=completed_registration.registration_number,
            completed_at=(
                completed_registration.completed_at.isoformat()
                if completed_registration.completed_at
                else None
            ),
            registration_status=completed_registration.registration_status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=RegistrationCompletionData(
                registration_id=completed_registration.uuid,
                completed=completed_registration.is_completed,
                completed_at=completed_registration.completed_at,
                event_id=event.event_id,
            ),
        )


__all__ = (
    "RegistrationCompletionData",
    "RegistrationCompletionRequest",
    "RegistrationCompletionWorkflow",
)
