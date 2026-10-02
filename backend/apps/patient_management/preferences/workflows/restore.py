"""Patient Preference restore workflow."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.preferences.events import PatientPreferenceRestoredEvent
from apps.patient_management.preferences.models import PatientPreference
from apps.patient_management.preferences.policies import PatientPreferencePolicy
from apps.patient_management.preferences.services import PatientPreferenceService
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientPreferenceRestoreRequest:
    """Input for preference restoration."""

    organization_id: UUID
    preference_id: UUID


class PatientPreferenceRestoreWorkflow(
    BaseWorkflow[UUID],
):
    """Restore one deleted patient preference."""

    def __init__(self, *, request, policy=None) -> None:
        """Initialize the workflow."""

        super().__init__()
        self._request = request
        self._policy = policy or PatientPreferencePolicy()

    @transaction.atomic
    def _run(self, *, context: WorkflowContext):
        """Execute the restoration transaction."""

        try:
            actor = User.objects.get(pk=context.actor_id)
            preference = PatientPreference.all_objects.select_related(
                "patient",
                "organization",
            ).get(
                id=self._request.preference_id,
                organization_id=self._request.organization_id,
                organization__tenant_id=context.tenant_id,
                is_deleted=True,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Deleted patient preference was not found.") from exc

        if not self._policy.can_restore(
            actor=actor,
            preference=preference,
        ):
            raise PermissionError(
                "User does not have permission to restore patient preferences.",
            )

        PatientPreferenceService.restore(preference=preference)

        event = PatientPreferenceRestoredEvent(
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
            message="Patient preferences restored successfully.",
        )


__all__ = (
    "PatientPreferenceRestoreRequest",
    "PatientPreferenceRestoreWorkflow",
)
