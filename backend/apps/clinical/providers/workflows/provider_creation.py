"""
Provider creation workflow.

Coordinates provider creation process.

Responsibilities:

- Resolve actor
- Resolve organization
- Validate RBAC policy
- Execute provider service
- Publish domain event
- Dispatch post commit tasks
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from apps.clinical.providers.events import (
    ProviderCreatedEvent,
)
from apps.clinical.providers.policies import (
    ProviderPolicy,
)
from apps.clinical.providers.services import (
    create_provider,
)
from apps.clinical.providers.tasks import (
    index_provider,
    send_provider_created_notification,
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
class ProviderCreationRequest:
    """
    Provider creation request.
    """

    organization_id: UUID

    employee_id: UUID

    provider_number: str

    provider_type: str

    years_of_experience: int = 0

    bio: str = ""

    is_accepting_patients: bool = True


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderCreationData:
    """
    Provider creation result.
    """

    provider_id: UUID

    created: bool

    event_id: UUID | None = None


class ProviderCreationWorkflow(
    BaseWorkflow[ProviderCreationData],
):
    """
    Creates provider profile.

    Flow:

        Actor
          |
          v
        RBAC Policy
          |
          v
        Provider Service
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
        request: ProviderCreationRequest,
        policy: ProviderPolicy | None = None,
    ) -> None:

        super().__init__()

        self._request = request

        self._policy = policy or ProviderPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[ProviderCreationData]:
        """
        Execute provider creation.
        """

        from apps.organization.employees.models import Employee
        from apps.platform.accounts.models import User
        from apps.platform.organizations.models import Organization

        actor = User.objects.get(
            id=context.actor_id,
        )

        organization = Organization.objects.get(
            id=self._request.organization_id,
        )

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to create provider.",
            )

        employee = Employee.objects.get(
            id=self._request.employee_id,
            organization_id=organization.id,
        )

        provider = create_provider(
            validated_data={
                "organization": organization,
                "employee": employee,
                "provider_number": (self._request.provider_number),
                "provider_type": (self._request.provider_type),
                "years_of_experience": (self._request.years_of_experience),
                "bio": (self._request.bio),
                "is_accepting_patients": (self._request.is_accepting_patients),
            },
        )

        event = ProviderCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            provider_id=provider.id,
            organization_id=organization.id,
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
            send_provider_created_notification,
            provider_id=provider.id,
        )

        logger.info(
            "Provider created.",
            extra={
                "provider_id": str(
                    provider.id,
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
            data=ProviderCreationData(
                provider_id=provider.id,
                created=True,
                event_id=event.event_id,
            ),
            message=("Provider created successfully."),
            code="provider_created",
        )


__all__ = (
    "ProviderCreationRequest",
    "ProviderCreationData",
    "ProviderCreationWorkflow",
)
