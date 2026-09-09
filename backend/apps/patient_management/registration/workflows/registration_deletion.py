"""
Patient Registration deletion workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows.base import BaseWorkflow
from apps.core.workflows.context import WorkflowContext
from apps.core.workflows.result import WorkflowResult
from apps.patient_management.registration.events.registration_deleted import (
    RegistrationDeletedEvent,
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
class RegistrationDeletionRequest:
    """
    Input contract for deleting a patient registration.
    """

    organization_id: UUID
    registration_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationDeletionData:
    """
    Result data returned by the Registration deletion workflow.
    """

    registration_id: UUID
    deleted: bool
    event_id: UUID | None = None


class RegistrationDeletionWorkflow(
    BaseWorkflow[RegistrationDeletionData],
):
    """
    Orchestrates authorization and domain mutation for Registration
    deletion.

    The workflow owns actor resolution, tenant scoping, authorization,
    service invocation, and domain-event publication.
    """

    workflow_name = "registration.delete"

    def __init__(
        self,
        *,
        request: RegistrationDeletionRequest,
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
    ) -> WorkflowResult[RegistrationDeletionData]:
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

        if not self._policy.can_delete(
            actor=actor,
            organization=organization,
            registration=registration,
        ):
            raise PermissionError(
                "You do not have permission to delete this patient registration."
            )

        registration_id = registration.uuid
        patient_id = registration.patient_id
        organization_id = registration.organization_id
        registration_number = registration.registration_number

        PatientRegistrationService.delete(
            instance=registration,
            performed_by=actor,
        )

        event = RegistrationDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            registration_id=registration_id,
            patient_id=patient_id,
            organization_id=organization_id,
            registration_number=registration_number,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=RegistrationDeletionData(
                registration_id=registration_id,
                deleted=True,
                event_id=event.event_id,
            ),
        )


__all__ = (
    "RegistrationDeletionData",
    "RegistrationDeletionRequest",
    "RegistrationDeletionWorkflow",
)
