"""
Emergency Contact update workflow.
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
from apps.patient_management.emergency_contacts.events import (
    EmergencyContactUpdatedEvent,
)
from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)
from apps.patient_management.emergency_contacts.policies import (
    EmergencyContactPolicy,
)
from apps.patient_management.emergency_contacts.services import (
    update_emergency_contact,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactUpdateRequest:
    emergency_contact_id: UUID
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True, kw_only=True)
class EmergencyContactUpdateData:
    emergency_contact_id: UUID
    updated: bool
    event_id: UUID | None = None


class EmergencyContactUpdateWorkflow(
    BaseWorkflow[EmergencyContactUpdateData],
):
    workflow_name = "emergency_contact.update"

    def __init__(
        self,
        *,
        request: EmergencyContactUpdateRequest,
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
    ) -> WorkflowResult[EmergencyContactUpdateData]:
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

        if not self._policy.can_update(
            actor=actor,
            emergency_contact=emergency_contact,
        ):
            raise PermissionError(
                "User does not have permission to update this emergency contact.",
            )

        data = dict(
            self._request.data,
        )

        if not data:
            return WorkflowResult.ok(
                context=context,
                data=EmergencyContactUpdateData(
                    emergency_contact_id=emergency_contact.id,
                    updated=False,
                ),
                message="No emergency contact changes were supplied.",
                code="emergency_contact_unchanged",
            )

        updated = update_emergency_contact(
            instance=emergency_contact,
            validated_data=data,
            performed_by=actor,
        )

        event = EmergencyContactUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            emergency_contact_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            relationship=updated.relationship,
            status=updated.status,
            is_primary=updated.is_primary,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=EmergencyContactUpdateData(
                emergency_contact_id=updated.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Emergency contact updated successfully.",
            code="emergency_contact_updated",
        )


__all__ = (
    "EmergencyContactUpdateData",
    "EmergencyContactUpdateRequest",
    "EmergencyContactUpdateWorkflow",
)
