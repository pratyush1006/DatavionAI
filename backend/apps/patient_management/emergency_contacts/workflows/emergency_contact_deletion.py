"""
Emergency Contact deletion workflow.
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
    EmergencyContactDeletedEvent,
)
from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)
from apps.patient_management.emergency_contacts.policies import (
    EmergencyContactPolicy,
)
from apps.patient_management.emergency_contacts.services import (
    delete_emergency_contact,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactDeletionRequest:
    emergency_contact_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactDeletionData:
    emergency_contact_id: UUID
    deleted: bool
    event_id: UUID


class EmergencyContactDeletionWorkflow(
    BaseWorkflow[EmergencyContactDeletionData],
):
    workflow_name = "emergency_contact.delete"

    def __init__(
        self,
        *,
        request: EmergencyContactDeletionRequest,
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
    ) -> WorkflowResult[EmergencyContactDeletionData]:
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

        if not self._policy.can_delete(
            actor=actor,
            emergency_contact=emergency_contact,
        ):
            raise PermissionError(
                "User does not have permission to delete this emergency contact.",
            )

        emergency_contact_id = emergency_contact.id
        patient_id = emergency_contact.patient_id
        organization_id = emergency_contact.organization_id
        emergency_contact_number = emergency_contact.emergency_contact_number

        delete_emergency_contact(
            instance=emergency_contact,
            performed_by=actor,
        )

        event = EmergencyContactDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            emergency_contact_id=emergency_contact_id,
            patient_id=patient_id,
            organization_id=organization_id,
            emergency_contact_number=emergency_contact_number,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=EmergencyContactDeletionData(
                emergency_contact_id=emergency_contact_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Emergency contact deleted successfully.",
            code="emergency_contact_deleted",
        )


__all__ = (
    "EmergencyContactDeletionData",
    "EmergencyContactDeletionRequest",
    "EmergencyContactDeletionWorkflow",
)
