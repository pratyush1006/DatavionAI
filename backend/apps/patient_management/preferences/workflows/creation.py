"""Patient Preference creation workflow."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.patients.models import Patient
from apps.patient_management.preferences.events import PatientPreferenceCreatedEvent
from apps.patient_management.preferences.policies import PatientPreferencePolicy
from apps.patient_management.preferences.services import PatientPreferenceService
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPreferenceCreationRequest:
    """Input for Patient Preference creation."""

    organization_id: UUID
    patient_id: UUID
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPreferenceCreationData:
    """Output from Patient Preference creation."""

    preference_id: UUID
    created: bool
    event_id: UUID | None = None


class PatientPreferenceCreationWorkflow(
    BaseWorkflow[PatientPreferenceCreationData],
):
    """Create a patient preference inside the current tenant."""

    def __init__(self, *, request, policy=None) -> None:
        """Initialize the workflow."""

        super().__init__()
        self._request = request
        self._policy = policy or PatientPreferencePolicy()

    @transaction.atomic
    def _run(self, *, context: WorkflowContext):
        """Execute the creation transaction."""

        try:
            actor = User.objects.get(pk=context.actor_id)
            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
            patient = Patient.objects.select_related("organization").get(
                pk=self._request.patient_id,
                organization_id=organization.id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested actor, organization, or patient was not found.",
            ) from exc

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to create patient preferences.",
            )

        preference = PatientPreferenceService.create(
            patient=patient,
            organization=organization,
            validated_data=dict(self._request.data),
        )

        event = PatientPreferenceCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            organization_id=organization.id,
            preference_id=preference.id,
            patient_id=preference.patient_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientPreferenceCreationData(
                preference_id=preference.id,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient preferences created successfully.",
        )


__all__ = (
    "PatientPreferenceCreationData",
    "PatientPreferenceCreationRequest",
    "PatientPreferenceCreationWorkflow",
)
