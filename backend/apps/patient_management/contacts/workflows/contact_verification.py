"""
Patient Contact verification workflow.
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
    ContactVerifiedEvent,
)
from apps.patient_management.contacts.models import Contact
from apps.patient_management.contacts.policies import (
    ContactPolicy,
)
from apps.patient_management.contacts.services import (
    verify_contact,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactVerificationRequest:
    contact_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContactVerificationData:
    contact_id: UUID
    status: str
    verified: bool
    event_id: UUID | None = None


class ContactVerificationWorkflow(
    BaseWorkflow[ContactVerificationData],
):
    workflow_name = "contact.verify"

    def __init__(
        self,
        *,
        request: ContactVerificationRequest,
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
    ) -> WorkflowResult[ContactVerificationData]:
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

        if not self._policy.can_verify(
            actor=actor,
            contact=contact,
        ):
            raise PermissionError(
                "User does not have permission to verify this patient contact.",
            )

        previous_status = contact.status

        updated = verify_contact(
            instance=contact,
            performed_by=actor,
        )

        if previous_status == updated.status:
            return WorkflowResult.ok(
                context=context,
                data=ContactVerificationData(
                    contact_id=updated.id,
                    status=updated.status,
                    verified=True,
                    event_id=None,
                ),
                message="Patient contact is already verified.",
                code="contact_already_verified",
            )

        event = ContactVerifiedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            contact_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_status=previous_status,
            new_status=updated.status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=ContactVerificationData(
                contact_id=updated.id,
                status=updated.status,
                verified=True,
                event_id=event.event_id,
            ),
            message="Patient contact verified successfully.",
            code="contact_verified",
        )


__all__ = (
    "ContactVerificationData",
    "ContactVerificationRequest",
    "ContactVerificationWorkflow",
)
