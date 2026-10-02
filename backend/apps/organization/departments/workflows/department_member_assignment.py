"""
Department member assignment workflow.

Coordinates employee assignment into departments.
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
    DepartmentMemberAssignedEvent,
)
from apps.organization.departments.models import (
    Department,
)
from apps.organization.departments.services import (
    DepartmentMemberService,
)
from apps.organization.departments.tasks import (
    index_department,
    send_department_member_assigned_notification,
    synchronize_department,
)
from apps.organization.employees.models import (
    Employee,
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
class DepartmentMemberAssignmentRequest:
    """
    Department member assignment request.
    """

    department_id: UUID

    employee_id: UUID

    role_id: UUID | None = None

    title: str = ""

    is_primary: bool = False


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DepartmentMemberAssignmentData:
    """
    Assignment result.
    """

    department_id: UUID

    employee_id: UUID

    assigned: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class DepartmentMemberAssignmentWorkflow(
    BaseWorkflow[DepartmentMemberAssignmentData],
):
    """
    Assigns employee to department.
    """

    def __init__(
        self,
        *,
        request: DepartmentMemberAssignmentRequest,
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
    ) -> WorkflowResult[DepartmentMemberAssignmentData]:
        """
        Execute member assignment.
        """

        department = Department.objects.get(
            organization_id=context.tenant_id,
            id=self._request.department_id,
        )

        employee = Employee.objects.get(
            id=self._request.employee_id,
        )

        role = None

        if self._request.role_id:
            from apps.organization.departments.models import (
                DepartmentRole,
            )

            role = DepartmentRole.objects.get(
                id=self._request.role_id,
                department=department,
            )

        DepartmentMemberService.assign(
            department=department,
            employee=employee,
            role=role,
            title=self._request.title,
            is_primary=self._request.is_primary,
        )

        event = DepartmentMemberAssignedEvent(
            department_id=department.id,
            employee_id=employee.id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            send_department_member_assigned_notification,
            department_id=department.id,
            employee_id=employee.id,
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
            "Department member assigned.",
            extra={
                "department_id": str(
                    department.id,
                ),
                "employee_id": str(
                    employee.id,
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
            data=DepartmentMemberAssignmentData(
                department_id=department.id,
                employee_id=employee.id,
                assigned=True,
                event_id=event.event_id,
            ),
            message=("Employee assigned to department successfully."),
            code=("department_member_assigned"),
        )


__all__ = (
    "DepartmentMemberAssignmentRequest",
    "DepartmentMemberAssignmentData",
    "DepartmentMemberAssignmentWorkflow",
)
