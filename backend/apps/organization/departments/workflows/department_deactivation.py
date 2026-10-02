"""
Department deactivation workflow.

Coordinates department deactivation through:

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
class DepartmentDeactivationRequest:
    """
    Department deactivation request.
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
class DepartmentDeactivationData:
    """
    Department deactivation result.
    """

    department_id: UUID

    deactivated: bool


# ============================================================
# Workflow
# ============================================================


class DepartmentDeactivationWorkflow(
    BaseWorkflow[DepartmentDeactivationData],
):
    """
    Deactivates department.
    """

    def __init__(
        self,
        *,
        request: DepartmentDeactivationRequest,
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
    ) -> WorkflowResult[DepartmentDeactivationData]:
        """
        Execute deactivation workflow.
        """

        department = Department.objects.get(
            organization_id=context.tenant_id,
            id=self._request.department_id,
        )

        department = DepartmentService.deactivate(
            instance=department,
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
            "Department deactivated.",
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
            data=DepartmentDeactivationData(
                department_id=department.id,
                deactivated=True,
            ),
            message=("Department deactivated successfully."),
            code=("department_deactivated"),
        )


__all__ = (
    "DepartmentDeactivationRequest",
    "DepartmentDeactivationData",
    "DepartmentDeactivationWorkflow",
)
