"""Patient Preference deletion workflow."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.preferences.events import PatientPreferenceDeletedEvent
from apps.patient_management.preferences.policies import PatientPreferencePolicy
from apps.patient_management.preferences.selectors import PatientPreferenceSelector
from apps.patient_management.preferences.services import PatientPreferenceService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPreferenceDeletionRequest:
    """Input for preference deletion."""

    organization_id: UUID
    preference_id: UUID


class PatientPreferenceDeletionWorkflow(
    BaseWorkflow[UUID],
):
    """Soft-delete one patient preference."""

    def __init__(self, *, request, policy=None) -> None:
        """Initialize the workflow."""

        super().__init__()
        self._request = request
        self._policy = policy or PatientPreferencePolicy()

    @transaction.atomic
    def _run(self, *, context: WorkflowContext):
        """Execute the deletion transaction."""

        try:
            actor = User.objects.get(pk=context.actor_id)
            preference = PatientPreferenceSelector.get(
                preference_id=self._request.preference_id,
                organization_id=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Patient preference was not found.") from exc

        if not self._policy.can_delete(
            actor=actor,
            preference=preference,
        ):
            raise PermissionError(
                "User does not have permission to delete patient preferences.",
            )

        PatientPreferenceService.delete(
            preference=preference,
            user_id=actor.id,
        )

        event = PatientPreferenceDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            organization_id=preference.organization_id,
            preference_id=preference.id,
            patient_id=preference.patient_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=preference.id,
            message="Patient preferences deleted successfully.",
        )


__all__ = (
    "PatientPreferenceDeletionRequest",
    "PatientPreferenceDeletionWorkflow",
)
