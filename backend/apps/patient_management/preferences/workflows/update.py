"""Patient Preference update workflow."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.preferences.events import PatientPreferenceUpdatedEvent
from apps.patient_management.preferences.policies import PatientPreferencePolicy
from apps.patient_management.preferences.selectors import PatientPreferenceSelector
from apps.patient_management.preferences.services import PatientPreferenceService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPreferenceUpdateRequest:
    """Input for Patient Preference updates."""

    organization_id: UUID
    preference_id: UUID
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPreferenceUpdateData:
    """Output from Patient Preference updates."""

    preference_id: UUID
    event_id: UUID | None = None


class PatientPreferenceUpdateWorkflow(
    BaseWorkflow[PatientPreferenceUpdateData],
):
    """Update one organization-scoped patient preference."""

    def __init__(self, *, request, policy=None) -> None:
        """Initialize the workflow."""

        super().__init__()
        self._request = request
        self._policy = policy or PatientPreferencePolicy()

    @transaction.atomic
    def _run(self, *, context: WorkflowContext):
        """Execute the update transaction."""

        try:
            actor = User.objects.get(pk=context.actor_id)
            preference = PatientPreferenceSelector.get(
                preference_id=self._request.preference_id,
                organization_id=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Patient preference was not found.") from exc

        if not self._policy.can_update(
            actor=actor,
            preference=preference,
        ):
            raise PermissionError(
                "User does not have permission to update patient preferences.",
            )

        preference = PatientPreferenceService.update(
            preference=preference,
            validated_data=dict(self._request.data),
        )

        event = PatientPreferenceUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            organization_id=preference.organization_id,
            preference_id=preference.id,
            patient_id=preference.patient_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientPreferenceUpdateData(
                preference_id=preference.id,
                event_id=event.event_id,
            ),
            message="Patient preferences updated successfully.",
        )


__all__ = (
    "PatientPreferenceUpdateData",
    "PatientPreferenceUpdateRequest",
    "PatientPreferenceUpdateWorkflow",
)
