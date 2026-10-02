"""
Organization offboarding workflow.

Coordinates organization offboarding by archiving the
organization and triggering cleanup/synchronization actions.

Business rules belong to domain services.
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
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.organizations.services.organization import (
    archive_organization,
)
from apps.platform.organizations.tasks.cleanup import (
    cleanup_orphaned_records,
)
from apps.platform.organizations.tasks.synchronization import (
    synchronize_organization,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationOffboardingRequest:
    """
    Organization offboarding request.
    """

    organization_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationOffboardingData:
    """
    Organization offboarding result.
    """

    organization_id: UUID

    archived: bool


class OrganizationOffboardingWorkflow(
    BaseWorkflow[OrganizationOffboardingData],
):
    """
    Coordinates organization offboarding.

    Steps:

    1. Validate workflow request
    2. Load organization
    3. Archive organization
    4. Cleanup orphaned records
    5. Synchronize external systems
    """

    def __init__(
        self,
        *,
        request: OrganizationOffboardingRequest,
        logger_: logging.Logger | None = None,
    ) -> None:

        super().__init__(
            logger_=logger_,
        )

        self._request = request

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[OrganizationOffboardingData]:
        """
        Execute organization offboarding workflow.
        """

        organization = self._get_organization(
            tenant_id=context.tenant_id,
            organization_id=self._request.organization_id,
        )

        organization = archive_organization(
            instance=organization,
        )

        self.dispatch_after_commit(
            cleanup_orphaned_records,
        )

        self.dispatch_after_commit(
            synchronize_organization,
            organization_id=organization.id,
        )

        logger.info(
            "Organization offboarding completed.",
            extra={
                "organization_id": str(
                    organization.id,
                ),
                "tenant_id": str(
                    context.tenant_id,
                ),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=OrganizationOffboardingData(
                organization_id=organization.id,
                archived=True,
            ),
            message=("Organization offboarding completed successfully."),
            code="organization_offboarding_completed",
        )

    def _get_organization(
        self,
        *,
        tenant_id: UUID,
        organization_id: UUID,
    ) -> Organization:
        """
        Load organization within tenant boundary.
        """

        return Organization.objects.get(
            id=organization_id,
            tenant_id=tenant_id,
        )


__all__: tuple[str, ...] = (
    "OrganizationOffboardingRequest",
    "OrganizationOffboardingData",
    "OrganizationOffboardingWorkflow",
)
