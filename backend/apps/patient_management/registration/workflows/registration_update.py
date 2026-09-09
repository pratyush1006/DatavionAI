"""
Patient Registration update workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows.base import BaseWorkflow
from apps.core.workflows.context import WorkflowContext
from apps.core.workflows.result import WorkflowResult
from apps.patient_management.registration.events.registration_updated import (
    RegistrationUpdatedEvent,
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
class RegistrationUpdateRequest:
    """
    Input contract for updating a patient registration.
    """

    organization_id: UUID
    registration_id: UUID
    data: dict[str, Any]


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationUpdateData:
    """
    Result data returned by the Registration update workflow.
    """

    registration_id: UUID
    updated: bool
    event_id: UUID | None = None


class RegistrationUpdateWorkflow(
    BaseWorkflow[RegistrationUpdateData],
):
    """
    Orchestrates authorization and domain mutation for Registration updates.

    HTTP concerns, serializer behavior, persistence details, and event
    publication are intentionally kept outside the API layer.

    Free-form notes may be persisted by the domain service, but they are
    intentionally excluded from the domain event payload.
    """

    workflow_name = "registration.update"

    _EVENT_EXCLUDED_FIELDS = frozenset(
        {
            "notes",
        }
    )

    def __init__(
        self,
        *,
        request: RegistrationUpdateRequest,
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
    ) -> WorkflowResult[RegistrationUpdateData]:
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
                uuid=self._request.registration_id,
                organization_id=organization.pk,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested organization or registration was not found.",
            ) from exc

        if not self._policy.can_update(
            actor=actor,
            organization=organization,
            registration=registration,
        ):
            raise PermissionError(
                "You do not have permission to update this patient registration.",
            )

        data = dict(self._request.data)

        before = {
            field_name: getattr(
                registration,
                field_name,
            )
            for field_name in data
        }

        updated_registration = PatientRegistrationService.update(
            instance=registration,
            validated_data=data,
            performed_by=actor,
        )

        changes: dict[str, Any] = {}

        for field_name, old_value in before.items():
            new_value = getattr(
                updated_registration,
                field_name,
            )

            if old_value == new_value:
                continue

            if field_name in self._EVENT_EXCLUDED_FIELDS:
                continue

            changes[field_name] = {
                "old": self._serialize_value(old_value),
                "new": self._serialize_value(new_value),
            }

        event = RegistrationUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            registration_id=updated_registration.uuid,
            patient_id=updated_registration.patient_id,
            organization_id=updated_registration.organization_id,
            registration_number=updated_registration.registration_number,
            changes=changes,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=RegistrationUpdateData(
                registration_id=updated_registration.uuid,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient registration updated successfully.",
            code="registration_updated",
        )

    @staticmethod
    def _serialize_value(
        value: Any,
    ) -> Any:
        """
        Convert model-related values into event-safe representations.
        """

        if isinstance(value, UUID):
            return str(value)

        if hasattr(value, "isoformat"):
            try:
                return value.isoformat()
            except (
                AttributeError,
                TypeError,
                ValueError,
            ):
                pass

        return value


__all__ = (
    "RegistrationUpdateData",
    "RegistrationUpdateRequest",
    "RegistrationUpdateWorkflow",
)
