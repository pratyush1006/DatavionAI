"""
Patient Registration rejection workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows.base import BaseWorkflow
from apps.core.workflows.context import WorkflowContext
from apps.core.workflows.result import WorkflowResult
from apps.patient_management.registration.constants import RegistrationStatus
from apps.patient_management.registration.events.registration_rejected import (
    RegistrationRejectedEvent,
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
class RegistrationRejectionRequest:
    """
    Input contract for rejecting a patient registration.
    """

    organization_id: UUID
    registration_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationRejectionData:
    """
    Result data returned by the Registration rejection workflow.
    """

    registration_id: UUID
    rejected: bool
    event_id: UUID | None = None


class RegistrationRejectionWorkflow(
    BaseWorkflow[RegistrationRejectionData],
):
    """
    Orchestrates authorization and domain mutation for Registration
    rejection.

    The workflow owns:
    - actor resolution
    - tenant scoping
    - organization scoping
    - authorization
    - service invocation
    - domain-event publication
    """

    workflow_name = "registration.reject"

    def __init__(
        self,
        *,
        request: RegistrationRejectionRequest,
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
    ) -> WorkflowResult[RegistrationRejectionData]:
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

        if not self._policy.can_reject(
            actor=actor,
            organization=organization,
            registration=registration,
        ):
            raise PermissionError(
                "You do not have permission to reject this patient registration.",
            )

        rejected_registration = PatientRegistrationService.reject(
            instance=registration,
            performed_by=actor,
        )

        event = RegistrationRejectedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            registration_id=rejected_registration.uuid,
            patient_id=rejected_registration.patient_id,
            organization_id=rejected_registration.organization_id,
            registration_number=rejected_registration.registration_number,
            registration_status=rejected_registration.registration_status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=RegistrationRejectionData(
                registration_id=rejected_registration.uuid,
                rejected=(
                    rejected_registration.registration_status
                    == RegistrationStatus.REJECTED
                ),
                event_id=event.event_id,
            ),
            message="Patient registration rejected successfully.",
            code="registration_rejected",
        )


__all__ = (
    "RegistrationRejectionData",
    "RegistrationRejectionRequest",
    "RegistrationRejectionWorkflow",
)
