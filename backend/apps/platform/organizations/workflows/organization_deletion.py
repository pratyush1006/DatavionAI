"""
Organization archive workflow.

Coordinates organization archival by orchestrating policies,
domain services, domain events, and asynchronous tasks.

Deletion from a business perspective is implemented as
soft lifecycle archival.
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
    OrganizationDeletedEvent,
)
from apps.platform.organizations.models import Organization
from apps.platform.organizations.policies import (
    OrganizationPolicy,
)
from apps.platform.organizations.services.organization import (
    delete_organization,
)
from apps.platform.organizations.tasks import (
    cleanup_deleted_organizations,
    synchronize_organization,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationDeletionRequest:
    """
    Organization deletion request.

    Deletion means lifecycle archival.
    """

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationDeletionData:
    """
    Organization deletion workflow payload.

    Represents business deletion/archive.
    """

    organization_id: UUID

    archived: bool

    event_id: UUID | None = None


class OrganizationDeletionWorkflow(
    BaseWorkflow[OrganizationDeletionData],
):
    """
    Archive organization workflow.

    Responsibilities:

    - Validate authorization policy.
    - Execute archive/delete domain service.
    - Publish lifecycle event.
    - Dispatch cleanup and synchronization tasks.
    """

    def __init__(
        self,
        *,
        request: OrganizationDeletionRequest,
        policy: OrganizationPolicy | None = None,
    ) -> None:

        super().__init__()

        self._request = request

        self._policy = policy or OrganizationPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[OrganizationDeletionData]:
        """
        Execute organization archive workflow.
        """

        request = self._request

        organization = self._get_organization(
            tenant_id=context.tenant_id,
            organization_id=request.organization_id,
        )

        actor = self._get_actor(
            actor_id=context.actor_id,
        )

        if not self._policy.can_delete(
            actor=actor,
            organization=organization,
        ):
            return WorkflowResult.fail(
                context=context,
                code="permission_denied",
                message=("You do not have permission to delete this organization."),
            )

        #
        # Domain service performs archive.
        #
        delete_organization(
            instance=organization,
        )

        event = OrganizationDeletedEvent(
            organization_id=organization.id,
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            cleanup_deleted_organizations,
        )

        self.dispatch_after_commit(
            synchronize_organization,
            organization_id=organization.id,
        )

        return WorkflowResult.ok(
            context=context,
            data=OrganizationDeletionData(
                organization_id=organization.id,
                archived=True,
                event_id=event.event_id,
            ),
            message=("Organization archived successfully."),
            code="organization_archived",
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
    "OrganizationDeletionRequest",
    "OrganizationDeletionData",
    "OrganizationDeletionWorkflow",
)
