"""
Department settings update workflow.

Coordinates department configuration changes.
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
from apps.organization.departments.events import (
    DepartmentSettingsUpdatedEvent,
)
from apps.organization.departments.models import (
    Department,
    DepartmentSetting,
)
from apps.organization.departments.services import (
    DepartmentSettingsService,
)
from apps.organization.departments.tasks import (
    index_department,
    synchronize_department,
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
class DepartmentSettingsUpdateRequest:
    """
    Department settings update request.
    """

    department_id: UUID

    configuration: dict


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DepartmentSettingsUpdateData:
    """
    Department settings update result.
    """

    department_id: UUID

    updated: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class DepartmentSettingsUpdateWorkflow(
    BaseWorkflow[DepartmentSettingsUpdateData],
):
    """
    Updates department settings.
    """

    def __init__(
        self,
        *,
        request: DepartmentSettingsUpdateRequest,
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
    ) -> WorkflowResult[DepartmentSettingsUpdateData]:
        """
        Execute settings update.
        """

        department = Department.objects.get(
            organization_id=context.tenant_id,
            id=self._request.department_id,
        )

        try:
            settings = department.department_settings

        except DepartmentSetting.DoesNotExist:
            settings = DepartmentSettingsService.create_default(
                department=department,
            )

        settings = DepartmentSettingsService.update(
            instance=settings,
            configuration=(self._request.configuration),
        )

        event = DepartmentSettingsUpdatedEvent(
            department_id=department.id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            index_department,
            department_id=department.id,
        )

        self.dispatch_after_commit(
            synchronize_department,
            department_id=department.id,
        )

        logger.info(
            "Department settings updated.",
            extra={
                "department_id": str(
                    department.id,
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
            data=DepartmentSettingsUpdateData(
                department_id=department.id,
                updated=True,
                event_id=event.event_id,
            ),
            message=("Department settings updated successfully."),
            code=("department_settings_updated"),
        )


__all__ = (
    "DepartmentSettingsUpdateRequest",
    "DepartmentSettingsUpdateData",
    "DepartmentSettingsUpdateWorkflow",
)
