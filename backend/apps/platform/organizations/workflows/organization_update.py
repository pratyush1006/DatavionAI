"""
Organization update workflow.

Coordinates organization update operations by orchestrating policies,
domain services, domain events, and background tasks.

Business rules belong in the service layer.
Authorization belongs in the policy layer.
Persistence belongs in services/repositories.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.events import (
    OrganizationUpdatedEvent,
)
from apps.platform.organizations.models import Organization
from apps.platform.organizations.policies import (
    OrganizationPolicy,
)
from apps.platform.organizations.services.organization import (
    update_organization,
)
from apps.platform.organizations.tasks import (
    index_organization,
    synchronize_organization,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationUpdateRequest:
    """
    Organization update workflow request.
    """

    organization_id: UUID

    name: str | None = None

    slug: str | None = None

    email: str | None = None

    phone: str | None = None

    website: str | None = None

    description: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(
    frozen=True,
    slots=True,
)
class OrganizationUpdateData:
    """
    Organization update workflow payload.
    """

    organization_id: UUID

    updated: bool

    event_id: UUID | None = None


class OrganizationUpdateWorkflow(
    BaseWorkflow[OrganizationUpdateData],
):
    """
    Coordinates organization updates.

    Responsibilities:

    - Validate authorization policy
    - Execute organization update service
    - Publish organization updated event
    - Dispatch post commit tasks
    """

    def __init__(
        self,
        *,
        request: OrganizationUpdateRequest,
        policy: OrganizationPolicy | None = None,
    ) -> None:

        super().__init__()

        self._request = request

        self._policy = policy or OrganizationPolicy()

    @property
    def request(
        self,
    ) -> OrganizationUpdateRequest:
        """
        Return workflow request.
        """

        return self._request

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[OrganizationUpdateData]:
        """
        Execute organization update workflow.
        """

        request = self._request

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
        # organizations.update
        #
        if not self._policy.can_update(
            actor=actor,
            organization=organization,
        ):
            return WorkflowResult.fail(
                context=context,
                code="permission_denied",
                message=("You do not have permission to update this organization."),
            )

        #
        # Partial update payload.
        #
        # Only supplied fields are updated.
        #
        validated_data = {
            key: value
            for key, value in {
                "name": request.name,
                "slug": request.slug,
                "email": request.email,
                "phone": request.phone,
                "website": request.website,
                "description": request.description,
                "metadata": request.metadata,
            }.items()
            if value is not None
        }

        organization = update_organization(
            instance=organization,
            validated_data=validated_data,
        )

        event = OrganizationUpdatedEvent(
            organization_id=organization.id,
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            changed_fields=list(
                validated_data.keys(),
            ),
        )

        self.publish_after_commit(
            event,
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
            data=OrganizationUpdateData(
                organization_id=organization.id,
                updated=True,
                event_id=event.event_id,
            ),
            message=("Organization updated successfully."),
            code="organization_updated",
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
    "OrganizationUpdateRequest",
    "OrganizationUpdateData",
    "OrganizationUpdateWorkflow",
)
