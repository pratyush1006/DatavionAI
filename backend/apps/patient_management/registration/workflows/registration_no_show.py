"""
Patient Registration no-show workflow.
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
from apps.patient_management.registration.events.registration_no_show import (
    RegistrationNoShowEvent,
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
class RegistrationNoShowRequest:
    """
    Input contract for marking a patient registration as no-show.
    """

    organization_id: UUID
    registration_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationNoShowData:
    """
    Result data returned by the Registration no-show workflow.
    """

    registration_id: UUID
    no_show: bool
    event_id: UUID | None = None


class RegistrationNoShowWorkflow(
    BaseWorkflow[RegistrationNoShowData],
):
    """
    Orchestrates authorization and domain mutation for Registration
    no-show.

    The workflow owns:
    - actor resolution
    - tenant scoping
    - organization scoping
    - authorization
    - service invocation
    - domain-event publication
    """

    workflow_name = "registration.no_show"

    def __init__(
        self,
        *,
        request: RegistrationNoShowRequest,
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
    ) -> WorkflowResult[RegistrationNoShowData]:
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
                "The requested organization or registration was not found.",
            ) from exc

        if not self._policy.can_no_show(
            actor=actor,
            registration=registration,
        ):
            raise PermissionError(
                "You do not have permission to mark this patient registration as no-show.",
            )

        no_show_registration = PatientRegistrationService.no_show(
            instance=registration,
            performed_by=actor,
        )

        event = RegistrationNoShowEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            registration_id=no_show_registration.id,
            patient_id=no_show_registration.patient_id,
            organization_id=no_show_registration.organization_id,
            registration_number=no_show_registration.registration_number,
            registration_status=no_show_registration.registration_status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=RegistrationNoShowData(
                registration_id=no_show_registration.id,
                no_show=(
                    no_show_registration.registration_status
                    == RegistrationStatus.NO_SHOW
                ),
                event_id=event.event_id,
            ),
            message="Patient registration marked as no-show successfully.",
            code="registration_no_show",
        )


__all__ = (
    "RegistrationNoShowData",
    "RegistrationNoShowRequest",
    "RegistrationNoShowWorkflow",
)
