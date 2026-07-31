"""
Employee creation workflow.

Coordinates employee creation process.

Responsibilities:

- Resolve actor
- Resolve organization
- Validate RBAC policy
- Execute employee service
- Publish domain event
- Dispatch post commit tasks
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
    EmployeeCreatedEvent,
)
from apps.organization.employees.policies import (
    EmployeePolicy,
)
from apps.organization.employees.services import (
    create_employee,
)
from apps.organization.employees.tasks import (
    index_employee,
    send_employee_created_notification,
    synchronize_employee,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeCreationRequest:
    """
    Employee creation request.
    """

    organization_id: UUID

    employee_code: str

    designation: str

    joining_date: date

    user_id: UUID | None = None

    work_email: str | None = None

    phone_number: str | None = None

    employment_type: str | None = None

    status: str | None = None


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeCreationData:
    """
    Employee creation result.
    """

    employee_id: UUID

    created: bool

    event_id: UUID | None = None


class EmployeeCreationWorkflow(
    BaseWorkflow[EmployeeCreationData],
):
    """
    Creates employee.

    Flow:

        Actor
          |
          v
        RBAC Policy
          |
          v
        Domain Service
          |
          v
        Domain Event
          |
          v
        Async Tasks
    """

    def __init__(
        self,
        *,
        request: EmployeeCreationRequest,
        policy: EmployeePolicy | None = None,
    ) -> None:

        super().__init__()

        self._request = request

        self._policy = policy or EmployeePolicy()

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[EmployeeCreationData]:
        """
        Execute employee creation.
        """

        from apps.platform.accounts.models import User
        from apps.platform.organizations.models import Organization

        actor = User.objects.get(
            id=context.actor_id,
        )

        organization = Organization.objects.get(
            id=self._request.organization_id,
        )

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "User does not have permission to create employee.",
            )

        user = None

        if self._request.user_id:
            user = User.objects.get(
                id=self._request.user_id,
                organization_id=organization.id,
            )

        employee = create_employee(
            validated_data={
                "organization": organization,
                "user": user,
                "employee_code": (self._request.employee_code),
                "designation": (self._request.designation),
                "work_email": (self._request.work_email),
                "phone_number": (self._request.phone_number),
                "employment_type": (self._request.employment_type),
                "status": (self._request.status or "PENDING"),
                "joining_date": (self._request.joining_date),
            },
        )

        event = EmployeeCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            employee_id=employee.id,
            organization_id=organization.id,
        )

        self.publish_after_commit(
            event,
        )

        self.dispatch_after_commit(
            index_employee,
            employee_id=employee.id,
        )

        self.dispatch_after_commit(
            synchronize_employee,
            employee_id=employee.id,
        )

        self.dispatch_after_commit(
            send_employee_created_notification,
            employee_id=employee.id,
        )

        logger.info(
            "Employee created.",
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
            data=EmployeeCreationData(
                employee_id=employee.id,
                created=True,
                event_id=event.event_id,
            ),
            message=("Employee created successfully."),
            code="employee_created",
        )


__all__ = (
    "EmployeeCreationRequest",
    "EmployeeCreationData",
    "EmployeeCreationWorkflow",
)
