"""
Organization branding update workflow.

Coordinates organization branding updates by orchestrating
domain services, policies, events, and asynchronous actions.

Business rules belong to the service layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.platform.organizations.events import (
    BrandingUpdatedEvent,
)
from apps.platform.organizations.models import (
    OrganizationBranding,
)
from apps.platform.organizations.services.organization_branding import (
    update_branding,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationBrandingUpdateRequest:
    """
    Organization branding update request.
    """

    branding_id: UUID

    data: dict[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationBrandingUpdateData:
    """
    Organization branding update result payload.
    """

    branding_id: UUID

    updated: bool

    event_id: UUID | None = None


class OrganizationBrandingUpdateWorkflow(
    BaseWorkflow[OrganizationBrandingUpdateData],
):
    """
    Coordinates organization branding update.

    Responsibilities:

    - Load branding configuration
    - Execute branding service
    - Publish branding updated event
    - Return workflow result

    The workflow does not contain branding rules.
    """

    def _run(
        self,
        *,
        context: WorkflowContext,
        request: OrganizationBrandingUpdateRequest,
    ) -> WorkflowResult[OrganizationBrandingUpdateData]:
        """
        Execute branding update workflow.
        """

        branding = self._get_branding(
            tenant_id=context.tenant_id,
            branding_id=request.branding_id,
        )

        branding = update_branding(
            instance=branding,
            validated_data=request.data,
        )

        event = BrandingUpdatedEvent(
            organization_id=branding.organization_id,
            branding_id=branding.id,
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=OrganizationBrandingUpdateData(
                branding_id=branding.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Organization branding updated successfully.",
            code="organization_branding_updated",
        )

    def _get_branding(
        self,
        *,
        tenant_id: UUID,
        branding_id: UUID,
    ) -> OrganizationBranding:
        """
        Load organization branding.

        Replace with selector layer once branding selectors
        are introduced.
        """

        return OrganizationBranding.objects.get(
            id=branding_id,
            organization__tenant_id=tenant_id,
        )


__all__: tuple[str, ...] = (
    "OrganizationBrandingUpdateRequest",
    "OrganizationBrandingUpdateData",
    "OrganizationBrandingUpdateWorkflow",
)
