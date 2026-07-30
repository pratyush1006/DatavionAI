"""
Department activation workflow.

Activates departments through:

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
class DepartmentActivationRequest:
    """
    Department activation request.
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
class DepartmentActivationData:
    """
    Department activation workflow result.
    """

    department_id: UUID

    activated: bool


# ============================================================
# Workflow
# ============================================================


class DepartmentActivationWorkflow(
    BaseWorkflow[DepartmentActivationData],
):
    """
    Activates department.
    """

    def __init__(
        self,
        *,
        request: DepartmentActivationRequest,
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
    ) -> WorkflowResult[DepartmentActivationData]:
        """
        Execute activation workflow.
        """

        department = Department.objects.get(
            organization_id=context.tenant_id,
            id=self._request.department_id,
        )

        department = DepartmentService.activate(
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
            "Department activated.",
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
            data=DepartmentActivationData(
                department_id=department.id,
                activated=True,
            ),
            message=("Department activated successfully."),
            code=("department_activated"),
        )


__all__ = (
    "DepartmentActivationRequest",
    "DepartmentActivationData",
    "DepartmentActivationWorkflow",
)
