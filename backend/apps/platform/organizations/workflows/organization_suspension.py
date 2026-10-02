"""
Organization suspension workflow.

Coordinates organization suspension by orchestrating policies,
domain services, domain events, and asynchronous tasks.

Business rules belong to the domain service layer.
Authorization belongs to the policy layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.events import (
    OrganizationSuspendedEvent,
)
from apps.platform.organizations.models import Organization
from apps.platform.organizations.policies import (
    OrganizationPolicy,
)
from apps.platform.organizations.services.organization import (
    suspend_organization,
)
from apps.platform.organizations.tasks import (
    index_organization,
    send_organization_suspended_notification,
    synchronize_organization,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationSuspensionRequest:
    """
    Organization suspension request.
    """

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationSuspensionData:
    """
    Organization suspension result.
    """

    organization_id: UUID

    suspended: bool

    event_id: UUID | None = None


class OrganizationSuspensionWorkflow(
    BaseWorkflow[OrganizationSuspensionData],
):
    """
    Coordinates organization suspension.

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
        Domain Service
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
        request: OrganizationSuspensionRequest,
        policy: OrganizationPolicy | None = None,
    ) -> None:

        super().__init__()

        self.request = request

        self._policy = policy or OrganizationPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[OrganizationSuspensionData]:
        """
        Execute suspension workflow.
        """

        organization = self._get_organization(
            tenant_id=context.tenant_id,
            organization_id=self.request.organization_id,
        )

        actor = self._get_actor(
            actor_id=context.actor_id,
        )

        #
        # Authorization boundary.
        #
        # RBAC permission:
        # organizations.suspend
        #
        if not self._policy.can_suspend(
            actor=actor,
            organization=organization,
        ):
            return WorkflowResult.fail(
                context=context,
                code="permission_denied",
                message=("You do not have permission to suspend this organization."),
            )

        organization = suspend_organization(
            instance=organization,
        )

        event = OrganizationSuspendedEvent(
            organization_id=organization.id,
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            send_organization_suspended_notification,
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
            data=OrganizationSuspensionData(
                organization_id=organization.id,
                suspended=True,
                event_id=event.event_id,
            ),
            message=("Organization suspended successfully."),
            code="organization_suspended",
        )

    def _get_organization(
        self,
        *,
        tenant_id: UUID,
        organization_id: UUID,
    ) -> Organization:
        """
        Load organization inside tenant boundary.
        """

        return Organization.objects.get(
            tenant_id=tenant_id,
            id=organization_id,
        )

    def _get_actor(
        self,
        *,
        actor_id: UUID,
    ) -> User:
        """
        Load workflow actor.
        """

        return User.objects.get(
            id=actor_id,
        )


__all__: tuple[str, ...] = (
    "OrganizationSuspensionRequest",
    "OrganizationSuspensionData",
    "OrganizationSuspensionWorkflow",
)
