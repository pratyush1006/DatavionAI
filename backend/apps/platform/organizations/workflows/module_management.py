"""
Organization module management workflow.

Coordinates organization module entitlement operations
through domain services.

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
from apps.platform.organizations.models import (
    OrganizationModule,
)
from apps.platform.organizations.services.organization_module import (
    disable_module,
    enable_module,
    update_module,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationModuleManagementRequest:
    """
    Organization module management request.
    """

    module_id: UUID

    data: dict[str, Any] | None = None

    action: str = "update"


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationModuleManagementData:
    """
    Organization module management result.
    """

    module_id: UUID

    action: str

    updated: bool


class OrganizationModuleManagementWorkflow(
    BaseWorkflow[OrganizationModuleManagementData],
):
    """
    Coordinates organization module operations.

    Supported actions:

    - update
    - enable
    - disable
    """

    def _run(
        self,
        *,
        context: WorkflowContext,
        request: OrganizationModuleManagementRequest,
    ) -> WorkflowResult[OrganizationModuleManagementData]:
        """
        Execute module management workflow.
        """

        module = self._get_module(
            tenant_id=context.tenant_id,
            module_id=request.module_id,
        )

        action = request.action.lower()

        if action == "enable":
            module = enable_module(
                instance=module,
            )

        elif action == "disable":
            module = disable_module(
                instance=module,
            )

        elif action == "update":
            module = update_module(
                instance=module,
                validated_data=(request.data or {}),
            )

        else:
            return WorkflowResult.failure(
                context=context,
                message=(f"Unsupported module action: {action}"),
                code="invalid_module_action",
            )

        return WorkflowResult.ok(
            context=context,
            data=OrganizationModuleManagementData(
                module_id=module.id,
                action=action,
                updated=True,
            ),
            message=("Organization module updated successfully."),
            code=(f"organization_module_{action}"),
        )

    def _get_module(
        self,
        *,
        tenant_id: UUID,
        module_id: UUID,
    ) -> OrganizationModule:
        """
        Load organization module.

        Replace with selector layer when module
        selectors are introduced.
        """

        return OrganizationModule.objects.get(
            id=module_id,
            organization__tenant_id=tenant_id,
        )


__all__: tuple[str, ...] = (
    "OrganizationModuleManagementRequest",
    "OrganizationModuleManagementData",
    "OrganizationModuleManagementWorkflow",
)
