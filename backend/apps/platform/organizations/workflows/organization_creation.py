"""
Organization creation workflow.

Coordinates the organization creation process.

The workflow is responsible for:
- Policy validation
- Domain service orchestration
- Domain event publishing
- Background task scheduling

Business rules remain inside the domain service layer.
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
    OrganizationCreatedEvent,
)
from apps.platform.organizations.policies import (
    OrganizationPolicy,
)
from apps.platform.organizations.services.organization import (
    create_organization,
)
from apps.platform.organizations.tasks import (
    index_organization,
    send_organization_created_notification,
    synchronize_organization,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationCreationRequest:
    """
    Organization creation request.
    """

    organization_type: str

    name: str

    code: str

    slug: str

    email: str | None = None

    phone: str | None = None

    website: str | None = None

    description: str | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationCreationData:
    """
    Organization creation workflow payload.
    """

    organization_id: UUID

    created: bool

    event_id: UUID | None = None


class OrganizationCreationWorkflow(
    BaseWorkflow[OrganizationCreationData],
):
    """
    Coordinates organization creation.

    Responsibilities:

    - Validate creation policy
    - Execute organization creation service
    - Publish organization created event
    - Dispatch post-commit tasks
    """

    def __init__(
        self,
        *,
        request: OrganizationCreationRequest,
        policy: OrganizationPolicy | None = None,
    ) -> None:
        super().__init__()

        self._request = request

        self._policy = policy or OrganizationPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[OrganizationCreationData]:
        """
        Execute organization creation orchestration.
        """

        from apps.platform.accounts.models import User
        from apps.platform.tenancy.models import Tenant

        actor = User.objects.get(
            id=context.actor_id,
        )

        if not self._policy.can_create(
            actor=actor,
        ):
            raise PermissionError(
                "User does not have permission to create organization.",
            )

        tenant = Tenant.objects.get(
            id=context.tenant_id,
        )

        organization = create_organization(
            validated_data={
                "tenant": tenant,
                "organization_type": (self._request.organization_type),
                "name": self._request.name,
                "code": self._request.code,
                "slug": self._request.slug,
                "email": self._request.email,
                "phone": self._request.phone,
                "website": self._request.website,
                "description": self._request.description,
            },
        )

        event = OrganizationCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            organization_id=organization.id,
            organization_code=organization.code,
            organization_name=organization.name,
            organization_type=organization.organization_type,
            organization_category=organization.category,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            send_organization_created_notification,
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
            data=OrganizationCreationData(
                organization_id=organization.id,
                created=True,
                event_id=event.event_id,
            ),
            message="Organization created successfully.",
            code="organization_created",
        )


__all__: tuple[str, ...] = (
    "OrganizationCreationRequest",
    "OrganizationCreationData",
    "OrganizationCreationWorkflow",
)
