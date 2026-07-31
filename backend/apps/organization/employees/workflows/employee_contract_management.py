"""
Employee contract management workflow.

Coordinates employee contract lifecycle.

Responsibilities:

- Tenant scoped employee lookup
- RBAC authorization
- Execute contract service
- Publish contract lifecycle events
- Dispatch background tasks
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
    EmployeeContractCreatedEvent,
)
from apps.organization.employees.models import (
    Employee,
)
from apps.organization.employees.policies import (
    EmployeePolicy,
)
from apps.organization.employees.services import (
    create_employee_contract,
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
class EmployeeContractManagementRequest:
    """
    Employee contract management request.
    """

    employee_id: UUID

    contract_data: dict


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeContractManagementData:
    """
    Employee contract management result.
    """

    employee_id: UUID

    contract_id: UUID

    created: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class EmployeeContractManagementWorkflow(
    BaseWorkflow[EmployeeContractManagementData],
):
    """
    Manages employee contract lifecycle.

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
        Contract Service
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
        request: EmployeeContractManagementRequest,
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
    ) -> WorkflowResult[EmployeeContractManagementData]:
        """
        Execute contract management.
        """

        from apps.platform.accounts.models import User

        actor = User.objects.get(
            id=context.actor_id,
        )

        employee = Employee.objects.select_related(
            "organization",
        ).get(
            id=self._request.employee_id,
            organization__tenant_id=context.tenant_id,
        )

        if not self._policy.can_manage_contracts(
            actor=actor,
            employee=employee,
        ):
            raise PermissionError(
                "User does not have permission to manage employee contracts.",
            )

        contract = create_employee_contract(
            employee=employee,
            validated_data=self._request.contract_data,
        )

        event = EmployeeContractCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            employee_id=employee.id,
            contract_id=contract.id,
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
            "Employee contract created.",
            extra={
                "employee_id": str(employee.id),
                "contract_id": str(contract.id),
                "tenant_id": str(context.tenant_id),
                "actor_id": str(context.actor_id),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=EmployeeContractManagementData(
                employee_id=employee.id,
                contract_id=contract.id,
                created=True,
                event_id=event.event_id,
            ),
            message=("Employee contract created successfully."),
            code="employee_contract_created",
        )


__all__ = (
    "EmployeeContractManagementRequest",
    "EmployeeContractManagementData",
    "EmployeeContractManagementWorkflow",
)
