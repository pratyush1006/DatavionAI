"""Patient Communication Preference workflow."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.preferences.constants import PreferenceChannel
from apps.patient_management.preferences.events import (
    PatientCommunicationPreferenceUpdatedEvent,
)
from apps.patient_management.preferences.policies import PatientPreferencePolicy
from apps.patient_management.preferences.selectors import PatientPreferenceSelector
from apps.patient_management.preferences.services import PatientPreferenceService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientCommunicationPreferenceRequest:
    """Input for communication preference updates."""

    organization_id: UUID
    preference_id: UUID
    channel: str
    data: Mapping[str, Any]


class PatientCommunicationPreferenceWorkflow(
    BaseWorkflow[UUID],
):
    """Create or update one communication channel preference."""

    def __init__(self, *, request, policy=None) -> None:
        """Initialize the workflow."""

        super().__init__()
        self._request = request
        self._policy = policy or PatientPreferencePolicy()

    @transaction.atomic
    def _run(self, *, context: WorkflowContext):
        """Execute the communication preference transaction."""

        try:
            actor = User.objects.get(pk=context.actor_id)
            preference = PatientPreferenceSelector.get(
                preference_id=self._request.preference_id,
                organization_id=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Patient preference was not found.") from exc

        if not self._policy.can_manage_communication(
            actor=actor,
            preference=preference,
        ):
            raise PermissionError(
                "User does not have permission to manage communication preferences.",
            )

        allowed_channels = {item.value for item in PreferenceChannel}
        if self._request.channel not in allowed_channels:
            raise ValueError("Unsupported communication preference channel.")

        communication = PatientPreferenceService.set_communication_preference(
            preference=preference,
            channel=self._request.channel,
            validated_data=dict(self._request.data),
        )

        event = PatientCommunicationPreferenceUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            organization_id=preference.organization_id,
            preference_id=preference.id,
            communication_preference_id=communication.id,
            patient_id=preference.patient_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=communication.id,
            message="Communication preference updated successfully.",
        )


__all__ = (
    "PatientCommunicationPreferenceRequest",
    "PatientCommunicationPreferenceWorkflow",
)
