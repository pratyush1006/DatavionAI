"""
Organization settings update workflow.

Coordinates organization settings updates by orchestrating
domain services, domain events, and workflow execution.

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
    SettingsUpdatedEvent,
)
from apps.platform.organizations.models import (
    OrganizationSettings,
)
from apps.platform.organizations.services.organization_settings import (
    update_settings,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationSettingsUpdateRequest:
    """
    Organization settings update request.
    """

    settings_id: UUID

    data: dict[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationSettingsUpdateData:
    """
    Organization settings update result.
    """

    settings_id: UUID

    updated: bool

    event_id: UUID | None = None


class OrganizationSettingsUpdateWorkflow(
    BaseWorkflow[OrganizationSettingsUpdateData],
):
    """
    Coordinates organization settings update.

    Responsibilities:

    - Load organization settings
    - Execute settings service
    - Publish settings updated event
    - Return workflow result

    No settings business rules live here.
    """

    def _run(
        self,
        *,
        context: WorkflowContext,
        request: OrganizationSettingsUpdateRequest,
    ) -> WorkflowResult[OrganizationSettingsUpdateData]:
        """
        Execute settings update workflow.
        """

        settings = self._get_settings(
            tenant_id=context.tenant_id,
            settings_id=request.settings_id,
        )

        settings = update_settings(
            instance=settings,
            validated_data=request.data,
        )

        event = SettingsUpdatedEvent(
            organization_id=settings.organization_id,
            settings_id=settings.id,
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=OrganizationSettingsUpdateData(
                settings_id=settings.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Organization settings updated successfully.",
            code="organization_settings_updated",
        )

    def _get_settings(
        self,
        *,
        tenant_id: UUID,
        settings_id: UUID,
    ) -> OrganizationSettings:
        """
        Load organization settings.

        Replace with selector layer after selectors are finalized.
        """

        return OrganizationSettings.objects.get(
            id=settings_id,
            organization__tenant_id=tenant_id,
        )


__all__: tuple[str, ...] = (
    "OrganizationSettingsUpdateRequest",
    "OrganizationSettingsUpdateData",
    "OrganizationSettingsUpdateWorkflow",
)
