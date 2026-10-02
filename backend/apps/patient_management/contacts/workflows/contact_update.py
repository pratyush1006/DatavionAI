"""
Patient Contact update workflow.

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
    ContactUpdatedEvent,
)
from apps.patient_management.contacts.models import Contact
from apps.patient_management.contacts.policies import (
    ContactPolicy,
)
from apps.patient_management.contacts.services import (
    update_contact,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactUpdateRequest:
    contact_id: UUID
    data: Mapping[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactUpdateData:
    contact_id: UUID
    updated: bool
    event_id: UUID | None = None


class ContactUpdateWorkflow(
    BaseWorkflow[ContactUpdateData],
):
    workflow_name = "contact.update"

    def __init__(
        self,
        *,
        request: ContactUpdateRequest,
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
    ) -> WorkflowResult[ContactUpdateData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            contact = Contact.objects.select_related(
                "organization",
                "patient",
            ).get(
                pk=self._request.contact_id,
                organization__tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested patient contact was not found.",
            ) from exc

        if not self._policy.can_update(
            actor=actor,
            contact=contact,
        ):
            raise PermissionError(
                "User does not have permission to update this patient contact.",
            )

        data = dict(self._request.data)

        if not data:
            return WorkflowResult.ok(
                context=context,
                data=ContactUpdateData(
                    contact_id=contact.id,
                    updated=False,
                ),
                message="No contact changes were supplied.",
                code="contact_unchanged",
            )

        updated = update_contact(
            instance=contact,
            validated_data=data,
            performed_by=actor,
        )

        event = ContactUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            contact_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            contact_type=updated.contact_type,
            purpose=updated.purpose,
            status=updated.status,
            is_primary=updated.is_primary,
            is_preferred=updated.is_preferred,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=ContactUpdateData(
                contact_id=updated.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient contact updated successfully.",
            code="contact_updated",
        )


__all__ = (
    "ContactUpdateData",
    "ContactUpdateRequest",
    "ContactUpdateWorkflow",
)
