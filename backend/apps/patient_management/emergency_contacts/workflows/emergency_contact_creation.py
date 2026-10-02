"""
Emergency Contact creation workflow.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, cast
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Manager

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.emergency_contacts.events import (
    EmergencyContactCreatedEvent,
)
from apps.patient_management.emergency_contacts.policies import (
    EmergencyContactPolicy,
)
from apps.patient_management.emergency_contacts.services import (
    create_emergency_contact,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactCreationRequest:
    organization_id: UUID
    patient_id: UUID
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactCreationData:
    emergency_contact_id: UUID
    created: bool
    event_id: UUID | None = None


class EmergencyContactCreationWorkflow(
    BaseWorkflow[EmergencyContactCreationData],
):
    workflow_name = "emergency_contact.create"

    def __init__(
        self,
        *,
        request: EmergencyContactCreationRequest,
        policy: EmergencyContactPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request
        self._policy = policy or EmergencyContactPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[EmergencyContactCreationData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )

            patient = cast(
                Manager[Patient],
                Patient._default_manager,
            ).get(
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
                "User does not have permission to create an emergency contact.",
            )

        data = dict(
            self._request.data,
        )

        data["organization"] = organization
        data["patient"] = patient

        emergency_contact = create_emergency_contact(
            validated_data=data,
            performed_by=actor,
        )

        event = EmergencyContactCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            emergency_contact_id=emergency_contact.id,
            patient_id=emergency_contact.patient_id,
            organization_id=emergency_contact.organization_id,
            emergency_contact_number=(emergency_contact.emergency_contact_number),
            relationship=emergency_contact.relationship,
            status=emergency_contact.status,
            is_primary=emergency_contact.is_primary,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=EmergencyContactCreationData(
                emergency_contact_id=emergency_contact.id,
                created=True,
                event_id=event.event_id,
            ),
            message="Emergency contact created successfully.",
            code="emergency_contact_created",
        )


__all__ = (
    "EmergencyContactCreationData",
    "EmergencyContactCreationRequest",
    "EmergencyContactCreationWorkflow",
)
