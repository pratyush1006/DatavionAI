"""
Employee deletion workflow.

Coordinates employee deletion lifecycle.

Responsibilities:

- Tenant scoped employee lookup
- RBAC authorization
- Validate employee lifecycle state
- Execute employee soft deletion
- Publish domain event
- Dispatch cleanup tasks
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
    EmployeeDeletedEvent,
)
from apps.organization.employees.models import (
    Employee,
)
from apps.organization.employees.policies import (
    EmployeePolicy,
)
from apps.organization.employees.services import (
    delete_employee,
)
from apps.organization.employees.tasks import (
    index_employee,
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
class EmployeeDeletionRequest:
    """
    Employee deletion request.
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
class EmployeeDeletionData:
    """
    Employee deletion result.
    """

    employee_id: UUID

    deleted: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class EmployeeDeletionWorkflow(
    BaseWorkflow[EmployeeDeletionData],
):
    """
    Deletes employee.

    Workflow:

        Actor
          |
          v
        Employee Lookup
          |
          v
        RBAC Policy
          |
          v
        Lifecycle Validation
          |
          v
        Soft Delete
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
        request: EmployeeDeletionRequest,
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
    ) -> WorkflowResult[EmployeeDeletionData]:
        """
        Execute employee deletion.
        """

        from apps.platform.accounts.models import User

        #
        # Resolve actor
        #
        actor = User.objects.get(
            id=context.actor_id,
        )

        #
        # Resolve employee
        #
        employee = Employee.objects.get(
            id=self._request.employee_id,
            organization__tenant_id=context.tenant_id,
        )

        #
        # RBAC authorization
        #
        if not self._policy.can_delete(
            actor=actor,
            employee=employee,
        ):
            raise PermissionError(
                "User does not have permission to delete employee.",
            )

        #
        # Lifecycle validation
        #
        if hasattr(
            employee,
            "status",
        ):
            if employee.status in {
                "ACTIVE",
                "PROBATION",
            }:
                raise ValueError(
                    "Employee must be offboarded before deletion.",
                )

        employee_id = employee.id

        organization_id = employee.organization_id

        #
        # Domain service
        #
        delete_employee(
            instance=employee,
        )

        #
        # Domain event
        #
        event = EmployeeDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            employee_id=employee_id,
            organization_id=organization_id,
        )

        self.publish_after_commit(
            event,
        )

        #
        # Background processing
        #
        self.dispatch_after_commit(
            index_employee,
            employee_id=employee_id,
        )

        self.dispatch_after_commit(
            synchronize_employee,
            employee_id=employee_id,
        )

        logger.info(
            "Employee deleted.",
            extra={
                "employee_id": str(
                    employee_id,
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
            data=EmployeeDeletionData(
                employee_id=employee_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message=("Employee deleted successfully."),
            code="employee_deleted",
        )


__all__ = (
    "EmployeeDeletionRequest",
    "EmployeeDeletionData",
    "EmployeeDeletionWorkflow",
)
