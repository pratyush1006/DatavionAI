"""
Organization restoration workflow.

Coordinates organization restoration by orchestrating policies,
domain services, domain events, and asynchronous tasks.

Business rules belong to the domain service layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.platform.organizations.events import (
    OrganizationRestoredEvent,
)
from apps.platform.organizations.policies import (
    OrganizationPolicy,
)
from apps.platform.organizations.services.organization import (
    restore_organization,
)
from apps.platform.organizations.tasks import (
    index_organization,
    send_organization_restored_notification,
    synchronize_organization,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationRestorationRequest:
    """
    Organization restoration request.
    """

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationRestorationData:
    """
    Organization restoration workflow result.
    """

    organization_id: UUID

    restored: bool

    event_id: UUID | None = None


class OrganizationRestorationWorkflow(
    BaseWorkflow[OrganizationRestorationData],
):
    """
    Coordinates organization restoration.

    Flow:

        WorkflowContext
              |
              v
        Load Actor
              |
              v
        Load Organization
              |
              v
        Authorization Policy
              |
              v
        Restore Service
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
        request: OrganizationRestorationRequest,
        policy: OrganizationPolicy | None = None,
    ) -> None:
        super().__init__(
            payload=request,
        )

        self._policy = policy or OrganizationPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
        request: OrganizationRestorationRequest | None = None,
    ) -> WorkflowResult[OrganizationRestorationData]:
        """
        Execute organization restoration workflow.
        """

        if request is None:
            request = self.payload

        if not isinstance(
            request,
            OrganizationRestorationRequest,
        ):
            raise TypeError("Invalid restoration workflow payload.")

        organization = self._get_organization(
            tenant_id=context.tenant_id,
            organization_id=request.organization_id,
        )

        actor = self._get_actor(
            actor_id=context.actor_id,
        )

        self._policy.can_restore(
            actor=actor,
            organization=organization,
        )

        organization = restore_organization(
            instance=organization,
        )

        event = OrganizationRestoredEvent(
            organization_id=organization.id,
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            send_organization_restored_notification,
            organization_id=organization.id,
        )

        self.dispatch_after_commit(
            index_organization,
            organization_id=organization.id,
        )

        self.dispatch_after_commit(
            synchronize_organization,
            organization_id=organization.id,
        )

        return WorkflowResult.ok(
            context=context,
            data=OrganizationRestorationData(
                organization_id=organization.id,
                restored=True,
                event_id=event.event_id,
            ),
            message="Organization restored successfully.",
            code="organization_restored",
        )

    def _get_organization(
        self,
        *,
        tenant_id: UUID,
        organization_id: UUID,
    ):
        """
        Load organization.
        """

        from apps.platform.organizations.models import Organization

        return Organization.objects.get(
            tenant_id=tenant_id,
            id=organization_id,
        )

    def _get_actor(
        self,
        *,
        actor_id: UUID,
    ):
        """
        Load workflow actor.
        """

        from apps.platform.accounts.models import User

        return User.objects.get(
            id=actor_id,
        )


__all__: tuple[str, ...] = (
    "OrganizationRestorationRequest",
    "OrganizationRestorationData",
    "OrganizationRestorationWorkflow",
)
