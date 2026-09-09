"""
Patient Registration creation workflow.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows.base import BaseWorkflow
from apps.core.workflows.context import WorkflowContext
from apps.core.workflows.result import WorkflowResult
from apps.patient_management.patients.models import Patient
from apps.patient_management.registration.events.registration_created import (
    RegistrationCreatedEvent,
)
from apps.patient_management.registration.policies.registration import (
    RegistrationPolicy,
)
from apps.patient_management.registration.services.registration import (
    PatientRegistrationService,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RegistrationCreationRequest:
    """
    Input contract for creating a patient registration.
    """

    organization_id: UUID
    patient_id: UUID
    data: Mapping[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RegistrationCreationData:
    """
    Result data returned by the Registration creation workflow.
    """

    registration_id: UUID
    created: bool
    event_id: UUID | None = None


class RegistrationCreationWorkflow(
    BaseWorkflow[RegistrationCreationData],
):
    """
    Orchestrates creation of a patient registration.

    The workflow owns:
    - actor resolution
    - tenant scoping
    - organization scoping
    - patient scoping
    - authorization
    - service invocation
    - domain-event publication
    """

    workflow_name = "registration.create"

    def __init__(
        self,
        *,
        request: RegistrationCreationRequest,
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
    ) -> WorkflowResult[RegistrationCreationData]:
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
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested organization or patient was not found.",
            ) from exc

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to create registration.",
            )

        data = dict(self._request.data)
        data["organization"] = organization
        data["patient"] = patient

        registration = PatientRegistrationService.create(
            validated_data=data,
            performed_by=actor,
        )

        event = RegistrationCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            registration_id=registration.uuid,
            patient_id=registration.patient_id,
            organization_id=registration.organization_id,
            registration_number=registration.registration_number,
            registration_type=registration.registration_type,
            registration_status=registration.registration_status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=RegistrationCreationData(
                registration_id=registration.uuid,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient registration created successfully.",
            code="registration_created",
        )


__all__ = (
    "RegistrationCreationData",
    "RegistrationCreationRequest",
    "RegistrationCreationWorkflow",
)
