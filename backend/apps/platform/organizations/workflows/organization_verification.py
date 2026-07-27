"""
Organization verification workflow.

Coordinates organization verification by orchestrating:

- Authorization policy
- Domain service
- Domain event
- Post commit tasks
- Workflow result handling

Business rules belong in services.
Authorization belongs in policies.
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
from apps.platform.accounts.models import User
from apps.platform.organizations.events import (
    OrganizationVerifiedEvent,
)
from apps.platform.organizations.models import Organization
from apps.platform.organizations.policies import (
    OrganizationPolicy,
)
from apps.platform.organizations.services.organization import (
    verify_organization,
)
from apps.platform.organizations.tasks import (
    index_organization,
    send_organization_verified_notification,
    synchronize_organization,
)

logger = logging.getLogger(__name__)


# ============================================================
# Request
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationVerificationRequest:
    """
    Organization verification request.
    """

    organization_id: UUID


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationVerificationData:
    """
    Organization verification workflow result.
    """

    organization_id: UUID

    verified: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class OrganizationVerificationWorkflow(
    BaseWorkflow[OrganizationVerificationData],
):
    """
    Organization verification workflow.

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
        Post Commit Tasks
    """

    def __init__(
        self,
        *,
        request: OrganizationVerificationRequest,
        policy: OrganizationPolicy | None = None,
        logger_: logging.Logger | None = None,
    ) -> None:

        super().__init__(
            logger_=logger_,
            payload=request,
        )

        self._request = request

        self._policy = policy or OrganizationPolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[OrganizationVerificationData]:
        """
        Execute organization verification.
        """

        organization = Organization.objects.get(
            tenant_id=context.tenant_id,
            id=self._request.organization_id,
        )

        actor = User.objects.get(
            id=context.actor_id,
        )

        #
        # Authorization
        #
        # RBAC permission:
        #
        # organizations.verify
        #
        if not self._policy.can_verify(
            actor=actor,
            organization=organization,
        ):
            return WorkflowResult.fail(
                context=context,
                code="permission_denied",
                message=("You do not have permission to verify this organization."),
            )

        #
        # Domain operation
        #
        organization = verify_organization(
            instance=organization,
        )

        #
        # Domain event
        #
        event = OrganizationVerifiedEvent(
            organization_id=organization.id,
            verification_status="verified",
        )

        self.publish_after_commit(
            event,
        )

        #
        # Async post commit actions
        #
        self.dispatch_after_commit(
            send_organization_verified_notification,
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

        logger.info(
            "Organization verified.",
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
            data=OrganizationVerificationData(
                organization_id=organization.id,
                verified=True,
                event_id=event.event_id,
            ),
            message=("Organization verified successfully."),
            code="organization_verified",
        )


__all__: tuple[str, ...] = (
    "OrganizationVerificationRequest",
    "OrganizationVerificationData",
    "OrganizationVerificationWorkflow",
)
