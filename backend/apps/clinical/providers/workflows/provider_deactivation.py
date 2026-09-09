"""
Provider deactivation workflow.

Coordinates provider deactivation lifecycle.

Responsibilities:

- Resolve actor
- Resolve provider
- Validate RBAC policy
- Validate lifecycle transition
- Deactivate provider
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
    ProviderDeactivatedEvent,
)
from apps.clinical.providers.policies import (
    ProviderPolicy,
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
class ProviderDeactivationRequest:
    """
    Provider deactivation request.
    """

    provider_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ProviderDeactivationData:
    """
    Provider deactivation result.
    """

    provider_id: UUID

    deactivated: bool

    event_id: UUID | None = None


class ProviderDeactivationWorkflow(
    BaseWorkflow[ProviderDeactivationData],
):
    """
    Deactivates provider.

    Allowed lifecycle transition:

        ACTIVE
          |
          v
        INACTIVE


    Flow:

        Actor
          |
          v
        RBAC Policy
          |
          v
        Lifecycle Validation
          |
          v
        Status Update
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
        request: ProviderDeactivationRequest,
        policy: ProviderPolicy | None = None,
    ) -> None:

        super().__init__()

        self._request = request

        self._policy = policy or ProviderPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[ProviderDeactivationData]:
        """
        Execute provider deactivation.
        """

        from apps.clinical.providers.models import Provider
        from apps.platform.accounts.models import User

        actor = User.objects.get(
            id=context.actor_id,
        )

        provider = Provider.objects.select_related(
            "organization",
        ).get(
            id=self._request.provider_id,
        )

        organization = provider.organization

        if not self._policy.can_deactivate(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to deactivate provider.",
            )

        self._validate_transition(
            provider,
        )

        provider.status = ProviderStatus.INACTIVE

        provider.full_clean()

        provider.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        event = ProviderDeactivatedEvent(
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
            send_provider_status_changed_notification,
            provider_id=provider.id,
        )

        logger.info(
            "Provider deactivated.",
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
            data=ProviderDeactivationData(
                provider_id=provider.id,
                deactivated=True,
                event_id=event.event_id,
            ),
            message=("Provider deactivated successfully."),
            code="provider_deactivated",
        )

    @staticmethod
    def _validate_transition(
        provider,
    ) -> None:
        """
        Validate provider lifecycle transition.

        Allowed:

            ACTIVE -> INACTIVE
        """

        if provider.status != ProviderStatus.ACTIVE:
            raise ValidationError(
                ("Provider cannot be deactivated from current status."),
            )


__all__ = (
    "ProviderDeactivationRequest",
    "ProviderDeactivationData",
    "ProviderDeactivationWorkflow",
)
