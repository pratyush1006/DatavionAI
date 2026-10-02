"""
Emergency Contact verification workflow.
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
from apps.patient_management.emergency_contacts.events import (
    EmergencyContactVerifiedEvent,
)
from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)
from apps.patient_management.emergency_contacts.policies import (
    EmergencyContactPolicy,
)
from apps.patient_management.emergency_contacts.services import (
    verify_emergency_contact,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactVerificationRequest:
    emergency_contact_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactVerificationData:
    emergency_contact_id: UUID
    verified: bool
    event_id: UUID | None = None


class EmergencyContactVerificationWorkflow(
    BaseWorkflow[EmergencyContactVerificationData],
):
    workflow_name = "emergency_contact.verify"

    def __init__(
        self,
        *,
        request: EmergencyContactVerificationRequest,
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
    ) -> WorkflowResult[EmergencyContactVerificationData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            emergency_contact = EmergencyContact.objects.select_related(
                "organization",
                "patient",
            ).get(
                pk=self._request.emergency_contact_id,
                organization__tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Emergency contact was not found.",
            ) from exc

        if not self._policy.can_verify(
            actor=actor,
            emergency_contact=emergency_contact,
        ):
            raise PermissionError(
                "User does not have permission to verify this emergency contact.",
            )

        previous_verified = emergency_contact.is_verified

        updated = verify_emergency_contact(
            instance=emergency_contact,
            performed_by=actor,
        )

        if previous_verified:
            return WorkflowResult.ok(
                context=context,
                data=EmergencyContactVerificationData(
                    emergency_contact_id=updated.id,
                    verified=True,
                ),
                message="Emergency contact is already verified.",
                code="emergency_contact_already_verified",
            )

        event = EmergencyContactVerifiedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            emergency_contact_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_verified=False,
            new_verified=True,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=EmergencyContactVerificationData(
                emergency_contact_id=updated.id,
                verified=True,
                event_id=event.event_id,
            ),
            message="Emergency contact verified successfully.",
            code="emergency_contact_verified",
        )


__all__ = (
    "EmergencyContactVerificationData",
    "EmergencyContactVerificationRequest",
    "EmergencyContactVerificationWorkflow",
)
