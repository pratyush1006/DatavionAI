"""
Department update workflow.

Coordinates department updates using:

- Tenant scoped lookup
- Domain service
- Domain event
- Post commit tasks
- Workflow result
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
    DepartmentUpdatedEvent,
)
from apps.organization.departments.models import (
    Department,
)
from apps.organization.departments.services import (
    DepartmentService,
)
from apps.organization.departments.tasks import (
    index_department,
    send_department_updated_notification,
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
class DepartmentUpdateRequest:
    """
    Department update request.
    """

    department_id: UUID

    data: dict


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DepartmentUpdateData:
    """
    Department update result.
    """

    department_id: UUID

    updated: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class DepartmentUpdateWorkflow(
    BaseWorkflow[DepartmentUpdateData],
):
    """
    Updates department.

    Workflow:

        Tenant Context
              |
              v
        Department Lookup
              |
              v
        Domain Service
              |
              v
        Domain Event
              |
              v
        Background Tasks
    """

    def __init__(
        self,
        *,
        request: DepartmentUpdateRequest,
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
    ) -> WorkflowResult[DepartmentUpdateData]:
        """
        Execute department update.
        """

        department = Department.objects.get(
            id=self._request.department_id,
            organization__tenant_id=context.tenant_id,
        )

        department = DepartmentService.update(
            instance=department,
            validated_data=self._request.data,
        )

        event = DepartmentUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            department_id=department.id,
            organization_id=department.organization_id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            send_department_updated_notification,
            department_id=department.id,
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
            "Department updated.",
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
            data=DepartmentUpdateData(
                department_id=department.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Department updated successfully.",
            code="department_updated",
        )


__all__ = (
    "DepartmentUpdateRequest",
    "DepartmentUpdateData",
    "DepartmentUpdateWorkflow",
)
