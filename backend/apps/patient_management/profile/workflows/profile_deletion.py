"""
Patient Profile deletion workflow.

Responsibilities
----------------
- Tenant-scoped profile lookup.
- RBAC authorization.
- Delegate deletion to ProfileService.
- Publish profile-deleted domain event.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.profile.events import (
    ProfileDeletedEvent,
)
from apps.patient_management.profile.models import (
    PatientProfile,
)
from apps.patient_management.profile.policies import (
    ProfilePolicy,
)
from apps.patient_management.profile.services import (
    delete_profile,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProfileDeletionRequest:
    """
    Patient Profile deletion request.
    """

    profile_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProfileDeletionData:
    """
    Patient Profile deletion result.
    """

    profile_id: UUID
    deleted: bool
    event_id: UUID | None = None


class ProfileDeletionWorkflow(
    BaseWorkflow[ProfileDeletionData],
):
    """
    Delete a patient profile.
    """

    def __init__(
        self,
        *,
        request: ProfileDeletionRequest,
        policy: ProfilePolicy | None = None,
        logger_: logging.Logger | None = None,
    ) -> None:
        super().__init__(
            logger_=logger_,
        )

        self._request = request
        self._policy = policy or ProfilePolicy()

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[ProfileDeletionData]:
        """
        Execute profile deletion.
        """

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

        if not self._policy.can_delete(
            actor=actor,
            profile=profile,
        ):
            raise PermissionError(
                "User does not have permission to delete patient profile.",
            )

        profile_id = profile.id
        patient_id = profile.patient_id
        organization_id = profile.organization_id

        delete_profile(
            instance=profile,
            performed_by=actor,
        )

        event = ProfileDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            profile_id=profile_id,
            patient_id=patient_id,
            organization_id=organization_id,
        )

        self.publish_after_commit(
            event,
        )

        self._logger.info(
            "Patient profile deleted.",
            extra={
                "workflow": "profile.delete",
                "profile_id": str(profile_id),
                "patient_id": str(patient_id),
                "organization_id": str(organization_id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=ProfileDeletionData(
                profile_id=profile_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Patient profile deleted successfully.",
            code="profile_deleted",
        )


__all__ = (
    "ProfileDeletionData",
    "ProfileDeletionRequest",
    "ProfileDeletionWorkflow",
)
