"""
Patient Profile creation workflow.

Responsibilities
----------------
- Resolve actor.
- Resolve tenant-scoped organization.
- Resolve tenant/organization-scoped patient.
- Validate RBAC policy.
- Delegate persistence to ProfileService.
- Publish profile-created domain event.

The workflow owns application orchestration.

The service owns domain validation and persistence.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.patients.models import (
    Patient,
)
from apps.patient_management.profile.events import (
    ProfileCreatedEvent,
)
from apps.patient_management.profile.policies import (
    ProfilePolicy,
)
from apps.patient_management.profile.services import (
    create_profile,
)
from apps.platform.organizations.models import (
    Organization,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProfileCreationRequest:
    """
    Patient Profile creation request.
    """

    organization_id: UUID
    patient_id: UUID
    data: Mapping[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProfileCreationData:
    """
    Patient Profile creation result.
    """

    profile_id: UUID
    created: bool
    event_id: UUID | None = None


class ProfileCreationWorkflow(
    BaseWorkflow[ProfileCreationData],
):
    """
    Create a patient profile inside the current tenant.
    """

    def __init__(
        self,
        *,
        request: ProfileCreationRequest,
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
    ) -> WorkflowResult[ProfileCreationData]:
        """
        Execute profile creation.
        """

        from apps.platform.accounts.models import User

        actor = User.objects.get(
            id=context.actor_id,
        )

        organization = Organization.objects.get(
            id=self._request.organization_id,
            tenant_id=context.tenant_id,
        )

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to create patient profile.",
            )

        patient = Patient.objects.select_related(
            "organization",
        ).get(
            id=self._request.patient_id,
            organization_id=organization.id,
        )

        validated_data = dict(
            self._request.data,
        )

        validated_data["organization"] = organization
        validated_data["patient"] = patient

        profile = create_profile(
            validated_data=validated_data,
            performed_by=actor,
        )

        event = ProfileCreatedEvent(
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
            "Patient profile created.",
            extra={
                "workflow": "profile.create",
                "profile_id": str(profile.id),
                "patient_id": str(profile.patient_id),
                "organization_id": str(profile.organization_id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=ProfileCreationData(
                profile_id=profile.id,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient profile created successfully.",
            code="profile_created",
        )


__all__ = (
    "ProfileCreationRequest",
    "ProfileCreationData",
    "ProfileCreationWorkflow",
)
