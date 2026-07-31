"""
Employee update workflow.

Coordinates employee updates using:

- Tenant scoped lookup
- RBAC policy
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
from apps.organization.employees.events import (
    EmployeeUpdatedEvent,
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
class EmployeeUpdateRequest:
    """
    Employee update request.
    """

    employee_id: UUID

    data: dict


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeUpdateData:
    """
    Employee update result.
    """

    employee_id: UUID

    updated: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class EmployeeUpdateWorkflow(
    BaseWorkflow[EmployeeUpdateData],
):
    """
    Updates employee.

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
        request: EmployeeUpdateRequest,
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
    ) -> WorkflowResult[EmployeeUpdateData]:
        """
        Execute employee update.
        """

        from apps.platform.accounts.models import User

        actor = User.objects.get(
            id=context.actor_id,
        )

        employee = Employee.objects.get(
            id=self._request.employee_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_manage(
            actor=actor,
            employee=employee,
        ):
            raise PermissionError(
                "User does not have permission to update employee.",
            )

        protected_fields = {
            "id",
            "organization",
            "organization_id",
            "employee_code",
            "joining_date",
        }

        validated_data = {
            key: value
            for key, value in self._request.data.items()
            if key not in protected_fields
        }

        employee = update_employee(
            instance=employee,
            validated_data=validated_data,
        )

        event = EmployeeUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            employee_id=employee.id,
            organization_id=employee.organization_id,
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
            "Employee updated.",
            extra={
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
            data=EmployeeUpdateData(
                employee_id=employee.id,
                updated=True,
                event_id=event.event_id,
            ),
            message=("Employee updated successfully."),
            code="employee_updated",
        )


__all__ = (
    "EmployeeUpdateRequest",
    "EmployeeUpdateData",
    "EmployeeUpdateWorkflow",
)
