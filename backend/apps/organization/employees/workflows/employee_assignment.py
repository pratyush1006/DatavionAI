"""
Employee assignment workflow.

Coordinates employee organizational assignment changes.

Responsibilities:

- Tenant scoped employee lookup
- RBAC authorization
- Resolve organization structure
- Execute assignment service
- Publish assignment event
- Dispatch background tasks
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.organization.employees.events import (
    EmployeeAssignmentChangedEvent,
)
from apps.organization.employees.models import (
    Employee,
    EmployeeAssignment,
)
from apps.organization.employees.policies import (
    EmployeePolicy,
)
from apps.organization.employees.services import (
    change_employee_assignment,
)
from apps.organization.employees.tasks import (
    index_employee,
    send_employee_updated_notification,
    synchronize_employee,
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
class EmployeeAssignmentRequest:
    """
    Employee assignment change request.
    """

    employee_id: UUID

    department_id: UUID

    team_id: UUID | None = None

    supervisor_id: UUID | None = None

    effective_from: date | None = None


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeAssignmentData:
    """
    Employee assignment change result.
    """

    employee_id: UUID

    assignment_id: UUID

    assigned: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class EmployeeAssignmentWorkflow(
    BaseWorkflow[EmployeeAssignmentData],
):
    """
    Updates employee organizational assignment.

    Workflow:

        Actor
          |
          v
        RBAC Policy
          |
          v
        Employee Lookup
          |
          v
        Assignment Service
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
        request: EmployeeAssignmentRequest,
        policy: EmployeePolicy | None = None,
        logger_: logging.Logger | None = None,
    ) -> None:

        super().__init__(
            logger_=logger_,
        )

        self._request = request

        self._policy = policy or EmployeePolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[EmployeeAssignmentData]:
        """
        Execute employee assignment update.
        """

        from apps.organization.departments.models import (
            Department,
        )
        from apps.organization.teams.models import (
            Team,
        )
        from apps.platform.accounts.models import (
            User,
        )

        actor = User.objects.get(
            id=context.actor_id,
        )

        employee = Employee.objects.select_related(
            "organization",
        ).get(
            id=self._request.employee_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_assign(
            actor=actor,
            employee=employee,
        ):
            raise PermissionError(
                "User does not have permission to assign employee.",
            )

        department = Department.objects.get(
            id=self._request.department_id,
            organization_id=employee.organization_id,
        )

        team = None

        if self._request.team_id:
            team = Team.objects.get(
                id=self._request.team_id,
                department_id=department.id,
            )

        supervisor = None

        if self._request.supervisor_id:
            supervisor = Employee.objects.get(
                id=self._request.supervisor_id,
                organization_id=employee.organization_id,
            )

        previous_assignment = EmployeeAssignment.objects.filter(
            employee=employee,
            is_current=True,
        ).first()

        assignment = change_employee_assignment(
            employee=employee,
            department=department,
            team=team,
            supervisor=supervisor,
            effective_from=(self._request.effective_from or date.today()),
        )

        event = EmployeeAssignmentChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            employee_id=employee.id,
            organization_id=employee.organization_id,
            previous_department_id=(
                previous_assignment.department_id if previous_assignment else None
            ),
            new_department_id=(assignment.department_id),
            previous_team_id=(
                previous_assignment.team_id if previous_assignment else None
            ),
            new_team_id=(assignment.team_id),
            previous_supervisor_id=(
                previous_assignment.supervisor_id if previous_assignment else None
            ),
            new_supervisor_id=(assignment.supervisor_id),
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            send_employee_updated_notification,
            employee_id=employee.id,
        )

        self.dispatch_after_commit(
            index_employee,
            employee_id=employee.id,
        )

        self.dispatch_after_commit(
            synchronize_employee,
            employee_id=employee.id,
        )

        logger.info(
            "Employee assignment changed.",
            extra={
                "employee_id": str(employee.id),
                "assignment_id": str(assignment.id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=EmployeeAssignmentData(
                employee_id=employee.id,
                assignment_id=assignment.id,
                assigned=True,
                event_id=event.event_id,
            ),
            message=("Employee assignment updated successfully."),
            code="employee_assignment_changed",
        )


__all__ = (
    "EmployeeAssignmentRequest",
    "EmployeeAssignmentData",
    "EmployeeAssignmentWorkflow",
)
