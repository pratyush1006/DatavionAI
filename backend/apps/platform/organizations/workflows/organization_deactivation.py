"""
Organization deactivation workflow.

Coordinates organization deactivation by orchestrating policies,
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
    OrganizationDeactivatedEvent,
)
from apps.platform.organizations.models import Organization
from apps.platform.organizations.policies import (
    OrganizationPolicy,
)
from apps.platform.organizations.services.organization import (
    deactivate_organization,
)
from apps.platform.organizations.tasks import (
    index_organization,
    send_organization_deactivated_notification,
    synchronize_organization,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationDeactivationRequest:
    """
    Organization deactivation request.
    """

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationDeactivationData:
    """
    Organization deactivation workflow payload.
    """

    organization_id: UUID

    deactivated: bool

    event_id: UUID | None = None


class OrganizationDeactivationWorkflow(
    BaseWorkflow[OrganizationDeactivationData],
):
    """
    Coordinates organization deactivation.

    Flow:

        Workflow Request
              |
              v
        Load Organization
              |
              v
        Load Actor
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
        request: OrganizationDeactivationRequest,
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
    ) -> WorkflowResult[OrganizationDeactivationData]:
        """
        Execute organization deactivation workflow.
        """

        request = self.payload

        if not isinstance(
            request,
            OrganizationDeactivationRequest,
        ):
            raise TypeError("Invalid deactivation workflow payload.")

        organization = self._get_organization(
            tenant_id=context.tenant_id,
            organization_id=request.organization_id,
        )

        actor = self._get_actor(
            actor_id=context.actor_id,
        )

        #
        # Authorization boundary.
        #
        # RBAC permission:
        # organizations.deactivate
        #
        if not self._policy.can_deactivate(
            actor=actor,
            organization=organization,
        ):
            return WorkflowResult.fail(
                context=context,
                code="permission_denied",
                message=("You do not have permission to deactivate this organization."),
            )

        organization = deactivate_organization(
            instance=organization,
        )

        event = OrganizationDeactivatedEvent(
            organization_id=organization.id,
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            send_organization_deactivated_notification,
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
            data=OrganizationDeactivationData(
                organization_id=organization.id,
                deactivated=True,
                event_id=event.event_id,
            ),
            message=("Organization deactivated successfully."),
            code="organization_deactivated",
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
    "OrganizationDeactivationRequest",
    "OrganizationDeactivationData",
    "OrganizationDeactivationWorkflow",
)
