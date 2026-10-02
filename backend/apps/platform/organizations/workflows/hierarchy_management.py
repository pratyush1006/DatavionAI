"""
Organization hierarchy management workflow.

Coordinates organization hierarchy relationship operations
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
    OrganizationHierarchy,
)
from apps.platform.organizations.services.organization_hierarchy import (
    delete_organization_hierarchy,
    update_organization_hierarchy,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationHierarchyManagementRequest:
    """
    Organization hierarchy management request.
    """

    hierarchy_id: UUID

    data: dict[str, Any] | None = None

    action: str = "update"


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationHierarchyManagementData:
    """
    Organization hierarchy management result.
    """

    hierarchy_id: UUID

    action: str

    updated: bool


class OrganizationHierarchyManagementWorkflow(
    BaseWorkflow[OrganizationHierarchyManagementData],
):
    """
    Coordinates organization hierarchy operations.

    Supported actions:

    - update
    - delete
    """

    def _run(
        self,
        *,
        context: WorkflowContext,
        request: OrganizationHierarchyManagementRequest,
    ) -> WorkflowResult[OrganizationHierarchyManagementData]:
        """
        Execute hierarchy management workflow.
        """

        hierarchy = self._get_hierarchy(
            tenant_id=context.tenant_id,
            hierarchy_id=request.hierarchy_id,
        )

        action = request.action.lower()

        if action == "delete":
            delete_organization_hierarchy(
                instance=hierarchy,
            )

        elif action == "update":
            hierarchy = update_organization_hierarchy(
                instance=hierarchy,
                validated_data=(request.data or {}),
            )

        else:
            return WorkflowResult.failure(
                context=context,
                message=(f"Unsupported hierarchy action: {action}"),
                code="invalid_hierarchy_action",
            )

        return WorkflowResult.ok(
            context=context,
            data=OrganizationHierarchyManagementData(
                hierarchy_id=request.hierarchy_id,
                action=action,
                updated=True,
            ),
            message=("Organization hierarchy updated successfully."),
            code=(f"organization_hierarchy_{action}"),
        )

    def _get_hierarchy(
        self,
        *,
        tenant_id: UUID,
        hierarchy_id: UUID,
    ) -> OrganizationHierarchy:
        """
        Load organization hierarchy.

        Replace with selector layer when hierarchy
        selectors are introduced.
        """

        return OrganizationHierarchy.objects.get(
            id=hierarchy_id,
            parent_organization__tenant_id=tenant_id,
        )


__all__: tuple[str, ...] = (
    "OrganizationHierarchyManagementRequest",
    "OrganizationHierarchyManagementData",
    "OrganizationHierarchyManagementWorkflow",
)
