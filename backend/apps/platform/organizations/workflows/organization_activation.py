"""
Organization activation workflow.

Activates an organization after successful creation
and onboarding.

Responsibilities:

- Resolve actor from workflow context
- Validate activation permission
- Activate organization
- Publish activation event
- Return workflow result
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.platform.accounts.models import (
    User,
)
from apps.platform.organizations.events import (
    OrganizationActivatedEvent,
)
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.organizations.policies import (
    OrganizationPolicy,
)
from apps.platform.organizations.services.organization import (
    activate_organization,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationActivationRequest:
    """
    Organization activation request.
    """

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationActivationData:
    """
    Organization activation workflow result.
    """

    organization_id: UUID

    activated: bool

    event_id: UUID | None = None


class OrganizationActivationWorkflow(
    BaseWorkflow[OrganizationActivationData],
):
    """
    Organization activation workflow.

    Responsibilities:

    - Resolve actor
    - Validate RBAC permission
    - Execute activation service
    - Publish activation event
    """

    def __init__(
        self,
        *,
        request: OrganizationActivationRequest,
        policy: OrganizationPolicy | None = None,
        logger_: logging.Logger | None = None,
    ) -> None:

        super().__init__(
            logger_=logger_,
        )

        self._request = request

        self._policy = policy or OrganizationPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[OrganizationActivationData]:
        """
        Execute organization activation.
        """

        organization = Organization.objects.get(
            tenant_id=context.tenant_id,
            id=self._request.organization_id,
        )

        actor = User.objects.get(
            id=context.actor_id,
        )

        #
        # Authorization boundary.
        #
        # RBAC permission:
        # organizations.activate
        #
        if not self._policy.can_activate(
            actor=actor,
            organization=organization,
        ):
            return WorkflowResult.fail(
                context=context,
                code="permission_denied",
                message=("You do not have permission to activate this organization."),
            )

        organization = activate_organization(
            instance=organization,
        )

        event = OrganizationActivatedEvent(
            organization_id=organization.id,
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        self.publish_after_commit(
            event,
        )

        data = OrganizationActivationData(
            organization_id=organization.id,
            activated=True,
            event_id=event.event_id,
        )

        logger.info(
            "Organization activated.",
            extra={
                "organization_id": str(
                    organization.id,
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
            data=data,
            message=("Organization activated successfully."),
            code="organization_activated",
        )


__all__: tuple[str, ...] = (
    "OrganizationActivationRequest",
    "OrganizationActivationData",
    "OrganizationActivationWorkflow",
)
