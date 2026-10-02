"""
Department deletion workflow.

Handles department archival lifecycle.

Responsibilities:

- Tenant scoped department lookup
- Execute archive service
- Publish department deleted event
- Schedule cleanup tasks
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
from apps.organization.departments.events import (
    DepartmentDeletedEvent,
)
from apps.organization.departments.models import (
    Department,
)
from apps.organization.departments.services import (
    DepartmentService,
)
from apps.organization.departments.tasks import (
    remove_department_index,
    send_department_deleted_notification,
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
class DepartmentDeletionRequest:
    """
    Department deletion request.
    """

    department_id: UUID


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DepartmentDeletionData:
    """
    Department deletion result.
    """

    department_id: UUID

    deleted: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class DepartmentDeletionWorkflow(
    BaseWorkflow[DepartmentDeletionData],
):
    """
    Archives department.

    Workflow:

        Tenant Context
              |
              v
        Department Lookup
              |
              v
        Archive Service
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
        request: DepartmentDeletionRequest,
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
    ) -> WorkflowResult[DepartmentDeletionData]:
        """
        Execute deletion workflow.
        """

        department = Department.objects.get(
            id=self._request.department_id,
            organization__tenant_id=context.tenant_id,
        )

        department = DepartmentService.archive(
            instance=department,
        )

        event = DepartmentDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            department_id=department.id,
            organization_id=department.organization_id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            send_department_deleted_notification,
            department_id=department.id,
        )

        self.dispatch_after_commit(
            remove_department_index,
            department_id=department.id,
        )

        self.dispatch_after_commit(
            synchronize_department,
            department_id=department.id,
        )

        logger.info(
            "Department deleted.",
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
            data=DepartmentDeletionData(
                department_id=department.id,
                deleted=True,
                event_id=event.event_id,
            ),
            message=("Department archived successfully."),
            code=("department_archived"),
        )


__all__ = (
    "DepartmentDeletionRequest",
    "DepartmentDeletionData",
    "DepartmentDeletionWorkflow",
)
