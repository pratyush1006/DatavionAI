"""
Patient Contact creation workflow.

Canonical mutation flow:
API → Workflow → Policy → Service → Domain Event.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.contacts.events import (
    ContactCreatedEvent,
)
from apps.patient_management.contacts.policies import (
    ContactPolicy,
)
from apps.patient_management.contacts.services import (
    create_contact,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactCreationRequest:
    organization_id: UUID
    patient_id: UUID
    data: Mapping[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactCreationData:
    contact_id: UUID
    created: bool
    event_id: UUID | None = None


class ContactCreationWorkflow(
    BaseWorkflow[ContactCreationData],
):
    workflow_name = "contact.create"

    def __init__(
        self,
        *,
        request: ContactCreationRequest,
        policy: ContactPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request
        self._policy = policy or ContactPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[ContactCreationData]:
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
                "User does not have permission to create a patient contact.",
            )

        data = dict(self._request.data)
        data["organization"] = organization
        data["patient"] = patient

        contact = create_contact(
            validated_data=data,
            performed_by=actor,
        )

        event = ContactCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            contact_id=contact.id,
            patient_id=contact.patient_id,
            organization_id=contact.organization_id,
            contact_type=contact.contact_type,
            purpose=contact.purpose,
            status=contact.status,
            is_primary=contact.is_primary,
            is_preferred=contact.is_preferred,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=ContactCreationData(
                contact_id=contact.id,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient contact created successfully.",
            code="contact_created",
        )


__all__ = (
    "ContactCreationData",
    "ContactCreationRequest",
    "ContactCreationWorkflow",
)
