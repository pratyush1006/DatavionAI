"""
Employee offboarding workflow.

Coordinates employee exit lifecycle.

Responsibilities:

- Resolve employee
- Deactivate employee
- Complete termination lifecycle
- Publish offboarding event
- Dispatch background tasks

This workflow orchestrates domain workflows.
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
from apps.organization.employees.constants import (
    EmploymentStatus,
)
from apps.organization.employees.events import (
    EmployeeOffboardedEvent,
)
from apps.organization.employees.models import (
    Employee,
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
class EmployeeOffboardingRequest:
    """
    Employee offboarding request.
    """

    employee_id: UUID

    termination_date: date | None = None


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeOffboardingData:
    """
    Employee offboarding result.
    """

    employee_id: UUID

    offboarded: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class EmployeeOffboardingWorkflow(
    BaseWorkflow[EmployeeOffboardingData],
):
    """
    Employee offboarding orchestration.

    Workflow:

        Employee Lookup
              |
              v
        Deactivation
              |
              v
        Termination
              |
              v
        Offboarded Event
              |
              v
        Background Tasks
    """

    def __init__(
        self,
        *,
        request: EmployeeOffboardingRequest,
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
    ) -> WorkflowResult[EmployeeOffboardingData]:
        """
        Execute employee offboarding.
        """

        from apps.organization.employees.workflows import (
            EmployeeDeactivationRequest,
            EmployeeDeactivationWorkflow,
        )

        #
        # Resolve employee
        #

        employee = Employee.objects.get(
            id=self._request.employee_id,
            organization__tenant_id=context.tenant_id,
        )

        #
        # Step 1
        # Deactivate employee
        #

        deactivation_result = EmployeeDeactivationWorkflow(
            request=EmployeeDeactivationRequest(
                employee_id=employee.id,
            ),
        ).execute(
            context=context,
        )

        #
        # Deactivation can be already completed.
        # Offboarding must remain idempotent.
        #

        if not deactivation_result.data:
            raise RuntimeError(
                "Employee deactivation failed during offboarding.",
            )

        #
        # Step 2
        # Complete employee termination lifecycle
        #

        employee.refresh_from_db()

        employee.status = EmploymentStatus.TERMINATED

        employee.is_active = False

        if self._request.termination_date:
            employee.termination_date = self._request.termination_date

        employee.save(
            update_fields=[
                "status",
                "is_active",
                "termination_date",
                "updated_at",
            ],
        )

        #
        # Domain event
        #

        event = EmployeeOffboardedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            employee_id=employee.id,
            organization_id=employee.organization_id,
        )

        self.publish_after_commit(
            event,
        )

        #
        # Background processing
        #

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
            "Employee offboarding completed.",
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
            data=EmployeeOffboardingData(
                employee_id=employee.id,
                offboarded=True,
                event_id=event.event_id,
            ),
            message=("Employee offboarded successfully."),
            code="employee_offboarded",
        )


__all__ = (
    "EmployeeOffboardingRequest",
    "EmployeeOffboardingData",
    "EmployeeOffboardingWorkflow",
)
