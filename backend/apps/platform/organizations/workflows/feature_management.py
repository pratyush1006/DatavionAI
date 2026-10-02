"""
Organization feature management workflow.

Coordinates organization feature entitlement operations
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
    OrganizationFeature,
)
from apps.platform.organizations.services.organization_feature import (
    disable_feature,
    enable_feature,
    update_feature,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationFeatureManagementRequest:
    """
    Organization feature management request.
    """

    feature_id: UUID

    data: dict[str, Any] | None = None

    action: str = "update"


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationFeatureManagementData:
    """
    Organization feature management result.
    """

    feature_id: UUID

    action: str

    updated: bool


class OrganizationFeatureManagementWorkflow(
    BaseWorkflow[OrganizationFeatureManagementData],
):
    """
    Coordinates organization feature operations.

    Supported actions:

    - update
    - enable
    - disable
    """

    def _run(
        self,
        *,
        context: WorkflowContext,
        request: OrganizationFeatureManagementRequest,
    ) -> WorkflowResult[OrganizationFeatureManagementData]:
        """
        Execute feature management workflow.
        """

        feature = self._get_feature(
            tenant_id=context.tenant_id,
            feature_id=request.feature_id,
        )

        action = request.action.lower()

        if action == "enable":
            feature = enable_feature(
                instance=feature,
            )

        elif action == "disable":
            feature = disable_feature(
                instance=feature,
            )

        elif action == "update":
            feature = update_feature(
                instance=feature,
                validated_data=(request.data or {}),
            )

        else:
            return WorkflowResult.failure(
                context=context,
                message=(f"Unsupported feature action: {action}"),
                code="invalid_feature_action",
            )

        return WorkflowResult.ok(
            context=context,
            data=OrganizationFeatureManagementData(
                feature_id=feature.id,
                action=action,
                updated=True,
            ),
            message=("Organization feature updated successfully."),
            code=(f"organization_feature_{action}"),
        )

    def _get_feature(
        self,
        *,
        tenant_id: UUID,
        feature_id: UUID,
    ) -> OrganizationFeature:
        """
        Load organization feature.

        Replace with selector layer when feature
        selectors are introduced.
        """

        return OrganizationFeature.objects.get(
            id=feature_id,
            organization__tenant_id=tenant_id,
        )


__all__: tuple[str, ...] = (
    "OrganizationFeatureManagementRequest",
    "OrganizationFeatureManagementData",
    "OrganizationFeatureManagementWorkflow",
)
