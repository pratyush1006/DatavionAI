"""
Employee deactivation workflow.

Deactivates an employee using:

- Tenant scoped lookup
- RBAC policy
- Lifecycle validation
- Domain service
- Domain event
- Post commit tasks
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
from apps.organization.employees.constants import (
    EmploymentStatus,
)
from apps.organization.employees.events import (
    EmployeeStatusChangedEvent,
)
from apps.organization.employees.models import (
    Employee,
)
from apps.organization.employees.policies import (
    EmployeePolicy,
)
from apps.organization.employees.services import (
    update_employee,
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
class EmployeeDeactivationRequest:
    """
    Employee deactivation request.
    """

    employee_id: UUID


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeDeactivationData:
    """
    Employee deactivation result.
    """

    employee_id: UUID

    deactivated: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class EmployeeDeactivationWorkflow(
    BaseWorkflow[EmployeeDeactivationData],
):
    """
    Deactivates employee.

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
        Status Transition
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
        request: EmployeeDeactivationRequest,
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
    ) -> WorkflowResult[EmployeeDeactivationData]:
        """
        Execute employee deactivation.
        """

        from apps.platform.accounts.models import User

        actor = User.objects.get(
            id=context.actor_id,
        )

        employee = Employee.objects.get(
            id=self._request.employee_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_deactivate(
            actor=actor,
            employee=employee,
        ):
            raise PermissionError(
                "User does not have permission to deactivate employee.",
            )

        previous_status = employee.status

        if previous_status == EmploymentStatus.SUSPENDED:
            return WorkflowResult.ok(
                context=context,
                data=EmployeeDeactivationData(
                    employee_id=employee.id,
                    deactivated=False,
                ),
                message=("Employee is already Suspended."),
                code="employee_already_suspended",
            )

        if previous_status == EmploymentStatus.TERMINATED:
            raise ValueError(
                "Terminated employees cannot be deactivated.",
            )

        employee = update_employee(
            instance=employee,
            validated_data={
                "status": (EmploymentStatus.SUSPENDED),
            },
        )

        event = EmployeeStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            employee_id=employee.id,
            organization_id=employee.organization_id,
            previous_status=previous_status,
            new_status=employee.status,
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
            "Employee deactivated.",
            extra={
                "employee_id": str(employee.id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=EmployeeDeactivationData(
                employee_id=employee.id,
                deactivated=True,
                event_id=event.event_id,
            ),
            message=("Employee deactivated successfully."),
            code="employee_deactivated",
        )


__all__ = (
    "EmployeeDeactivationRequest",
    "EmployeeDeactivationData",
    "EmployeeDeactivationWorkflow",
)
