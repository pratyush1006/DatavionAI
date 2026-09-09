"""
Patient Contact deletion workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.contacts.events import (
    ContactDeletedEvent,
)
from apps.patient_management.contacts.models import Contact
from apps.patient_management.contacts.policies import (
    ContactPolicy,
)
from apps.patient_management.contacts.services import (
    delete_contact,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactDeletionRequest:
    contact_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactDeletionData:
    contact_id: UUID
    deleted: bool
    event_id: UUID


class ContactDeletionWorkflow(
    BaseWorkflow[ContactDeletionData],
):
    workflow_name = "contact.delete"

    def __init__(
        self,
        *,
        request: ContactDeletionRequest,
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
    ) -> WorkflowResult[ContactDeletionData]:
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
                "Patient contact was not found.",
            ) from exc

        if not self._policy.can_delete(
            actor=actor,
            contact=contact,
        ):
            raise PermissionError(
                "User does not have permission to delete this patient contact.",
            )

        contact_id = contact.id
        patient_id = contact.patient_id
        organization_id = contact.organization_id
        contact_type = contact.contact_type
        purpose = contact.purpose

        delete_contact(
            instance=contact,
            performed_by=actor,
        )

        event = ContactDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            contact_id=contact_id,
            patient_id=patient_id,
            organization_id=organization_id,
            contact_type=contact_type,
            purpose=purpose,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=ContactDeletionData(
                contact_id=contact_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Patient contact deleted successfully.",
            code="contact_deleted",
        )


__all__ = (
    "ContactDeletionData",
    "ContactDeletionRequest",
    "ContactDeletionWorkflow",
)
