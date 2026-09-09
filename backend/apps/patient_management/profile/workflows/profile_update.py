"""
Patient Profile update workflow.

Responsibilities
----------------
- Tenant-scoped profile lookup.
- RBAC authorization.
- Enforce workflow-level update boundaries.
- Delegate mutation to ProfileService.
- Publish profile-updated domain event.

The workflow never performs direct model mutation.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.profile.events import (
    ProfileUpdatedEvent,
)
from apps.patient_management.profile.models import (
    PatientProfile,
)
from apps.patient_management.profile.policies import (
    ProfilePolicy,
)
from apps.patient_management.profile.services import (
    update_profile,
)

logger = logging.getLogger(__name__)


type ProfileUpdateDataMap = Mapping[str, object]


_ALLOWED_UPDATE_FIELDS = frozenset(
    {
        "preferred_language",
        "language_proficiency",
        "nationality",
        "religion",
        "ethnicity",
        "occupation",
        "employment_status",
        "education_level",
        "income_bracket",
        "interpreter_required",
    }
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProfileUpdateRequest:
    """
    Patient Profile update request.
    """

    profile_id: UUID
    data: ProfileUpdateDataMap


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProfileUpdateData:
    """
    Patient Profile update result.
    """

    profile_id: UUID
    updated: bool
    event_id: UUID | None = None


class ProfileUpdateWorkflow(
    BaseWorkflow[ProfileUpdateData],
):
    """
    Update a patient profile aggregate.
    """

    def __init__(
        self,
        *,
        request: ProfileUpdateRequest,
        policy: ProfilePolicy | None = None,
        logger_: logging.Logger | None = None,
    ) -> None:
        super().__init__(
            logger_=logger_,
        )

        self._request = request
        self._policy = policy or ProfilePolicy()

    def _validate_update_fields(self) -> None:
        """
        Enforce the workflow-level mutable-field boundary.
        """

        invalid_fields = frozenset(
            self._request.data,
        ).difference(
            _ALLOWED_UPDATE_FIELDS,
        )

        if invalid_fields:
            fields = ", ".join(
                sorted(
                    invalid_fields,
                ),
            )

            raise ValidationError(
                f"Patient profile update contains unsupported fields: {fields}.",
            )

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[ProfileUpdateData]:
        """
        Execute profile update.
        """

        self._validate_update_fields()

        if not self._request.data:
            return WorkflowResult.ok(
                context=context,
                data=ProfileUpdateData(
                    profile_id=self._request.profile_id,
                    updated=False,
                ),
                message="No patient profile changes were requested.",
                code="profile_update_no_changes",
            )

        from apps.platform.accounts.models import User

        actor = User.objects.get(
            id=context.actor_id,
        )

        profile = PatientProfile.objects.select_related(
            "organization",
            "patient",
        ).get(
            id=self._request.profile_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_manage(
            actor=actor,
            profile=profile,
        ):
            raise PermissionError(
                "User does not have permission to update patient profile.",
            )

        profile = update_profile(
            instance=profile,
            validated_data=self._request.data,
            performed_by=actor,
        )

        event = ProfileUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            profile_id=profile.id,
            patient_id=profile.patient_id,
            organization_id=profile.organization_id,
        )

        self.publish_after_commit(
            event,
        )

        self._logger.info(
            "Patient profile updated.",
            extra={
                "workflow": "profile.update",
                "profile_id": str(profile.id),
                "patient_id": str(profile.patient_id),
                "organization_id": str(profile.organization_id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=ProfileUpdateData(
                profile_id=profile.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient profile updated successfully.",
            code="profile_updated",
        )


__all__ = (
    "ProfileUpdateData",
    "ProfileUpdateRequest",
    "ProfileUpdateWorkflow",
)
