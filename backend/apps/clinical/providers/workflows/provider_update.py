"""
Provider update workflow.

Coordinates provider profile updates.

Responsibilities:

- Resolve actor
- Resolve provider
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
    ProviderUpdatedEvent,
)
from apps.clinical.providers.policies import (
    ProviderPolicy,
)
from apps.clinical.providers.services import (
    update_provider,
)
from apps.clinical.providers.tasks import (
    index_provider,
    send_provider_updated_notification,
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
class ProviderUpdateRequest:
    """
    Provider update request.
    """

    provider_id: UUID

    data: dict


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderUpdateData:
    """
    Provider update result.
    """

    provider_id: UUID

    updated: bool

    event_id: UUID | None = None


class ProviderUpdateWorkflow(
    BaseWorkflow[ProviderUpdateData],
):
    """
    Updates provider profile.

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
        request: ProviderUpdateRequest,
        policy: ProviderPolicy | None = None,
    ) -> None:

        super().__init__()

        self._request = request

        self._policy = policy or ProviderPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[ProviderUpdateData]:
        """
        Execute provider update.
        """

        from apps.clinical.providers.models import Provider
        from apps.platform.accounts.models import User
        from apps.platform.organizations.models import Organization

        actor = User.objects.get(
            id=context.actor_id,
        )

        provider = Provider.objects.select_related(
            "organization",
        ).get(
            id=self._request.provider_id,
        )

        organization = Organization.objects.get(
            id=provider.organization_id,
        )

        if not self._policy.can_update(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to update provider.",
            )

        provider = update_provider(
            instance=provider,
            validated_data=self._request.data,
        )

        event = ProviderUpdatedEvent(
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
            send_provider_updated_notification,
            provider_id=provider.id,
        )

        logger.info(
            "Provider updated.",
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
            data=ProviderUpdateData(
                provider_id=provider.id,
                updated=True,
                event_id=event.event_id,
            ),
            message=("Provider updated successfully."),
            code="provider_updated",
        )


__all__ = (
    "ProviderUpdateRequest",
    "ProviderUpdateData",
    "ProviderUpdateWorkflow",
)
