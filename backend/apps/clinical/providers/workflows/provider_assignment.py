"""
Provider assignment workflow.

Coordinates provider assignment lifecycle.

Responsibilities:

- Resolve actor
- Resolve organization
- Validate RBAC policy
- Validate provider eligibility
- Validate organization boundaries
- Create provider assignment
- Publish domain event
- Dispatch post commit tasks
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ValidationError

from apps.clinical.providers.constants import (
    ProviderStatus,
)
from apps.clinical.providers.events import (
    ProviderAssignedEvent,
)
from apps.clinical.providers.policies import (
    ProviderPolicy,
)
from apps.clinical.providers.services import (
    create_provider_assignment,
)
from apps.clinical.providers.tasks import (
    index_provider,
    send_provider_status_changed_notification,
    synchronize_provider,
)
from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderAssignmentRequest:
    """
    Provider assignment request.
    """

    provider_id: UUID

    organization_id: UUID

    department_id: UUID | None = None

    team_id: UUID | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderAssignmentData:
    """
    Provider assignment result.
    """

    assignment_id: UUID

    provider_id: UUID

    assigned: bool

    event_id: UUID | None = None


class ProviderAssignmentWorkflow(
    BaseWorkflow[ProviderAssignmentData],
):
    """
    Assign provider.

    Allowed lifecycle:

        VERIFIED
            |
            v
        ACTIVE
            |
            v
        ASSIGNMENT CREATED


    Flow:

        Actor
          |
          v
        RBAC Policy
          |
          v
        Provider Validation
          |
          v
        Assignment Service
          |
          v
        Domain Event
          |
          v
        Async Tasks
    """

    def __init__(
        self,
        *,
        request: ProviderAssignmentRequest,
        policy: ProviderPolicy | None = None,
    ) -> None:

        super().__init__()

        self._request = request

        self._policy = policy or ProviderPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[ProviderAssignmentData]:
        """
        Execute provider assignment.
        """

        from apps.clinical.providers.models import Provider
        from apps.organization.departments.models import Department
        from apps.organization.teams.models import Team
        from apps.platform.accounts.models import User
        from apps.platform.organizations.models import Organization

        actor = User.objects.get(
            id=context.actor_id,
        )

        organization = Organization.objects.get(
            id=self._request.organization_id,
        )

        if not self._policy.can_assign(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to assign provider.",
            )

        provider = Provider.objects.get(
            id=self._request.provider_id,
            organization_id=organization.id,
        )

        self._validate_provider(
            provider,
        )

        department = None

        if self._request.department_id:
            department = Department.objects.get(
                id=self._request.department_id,
                organization_id=organization.id,
            )

        team = None

        if self._request.team_id:
            team = Team.objects.get(
                id=self._request.team_id,
                organization_id=organization.id,
            )

        assignment = create_provider_assignment(
            validated_data={
                "organization": organization,
                "provider": provider,
                "department": department,
                "team": team,
            },
        )

        event = ProviderAssignedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            provider_id=provider.id,
            organization_id=organization.id,
            assignment_id=assignment.id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            index_provider,
            provider_id=provider.id,
        )

        self.dispatch_after_commit(
            synchronize_provider,
            provider_id=provider.id,
        )

        self.dispatch_after_commit(
            send_provider_status_changed_notification,
            provider_id=provider.id,
        )

        logger.info(
            "Provider assignment created.",
            extra={
                "provider_id": str(
                    provider.id,
                ),
                "assignment_id": str(
                    assignment.id,
                ),
                "tenant_id": str(
                    context.tenant_id,
                ),
                "actor_id": str(
                    context.actor_id,
                ),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=ProviderAssignmentData(
                assignment_id=assignment.id,
                provider_id=provider.id,
                assigned=True,
                event_id=event.event_id,
            ),
            message=("Provider assigned successfully."),
            code="provider_assigned",
        )

    @staticmethod
    def _validate_provider(
        provider,
    ) -> None:
        """
        Validate provider eligibility.

        Allowed:

            VERIFIED
            ACTIVE
        """

        if provider.status not in (
            ProviderStatus.VERIFIED,
            ProviderStatus.ACTIVE,
        ):
            raise ValidationError(
                "Provider must be verified before assignment.",
            )


__all__ = (
    "ProviderAssignmentRequest",
    "ProviderAssignmentData",
    "ProviderAssignmentWorkflow",
)
