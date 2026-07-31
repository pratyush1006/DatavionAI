"""
Employee onboarding workflow.

Coordinates complete employee onboarding lifecycle.

Responsibilities:

- Create employee identity
- Setup employment contract
- Setup organization assignment
- Activate employee
- Publish onboarding event
- Dispatch post commit tasks

Architecture:

Workflow
    |
    +--> EmployeeCreationWorkflow
    |
    +--> EmployeeContractManagementWorkflow
    |
    +--> EmployeeAssignmentWorkflow
    |
    +--> EmployeeActivationWorkflow
    |
    +--> EmployeeOnboardedEvent
    |
    +--> Background Tasks
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
    EmployeeOnboardedEvent,
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
class EmployeeOnboardingRequest:
    """
    Employee onboarding request.
    """

    organization_id: UUID

    employee_data: dict

    contract_data: dict | None = None

    assignment_data: dict | None = None


# ============================================================
# Result
# ============================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeOnboardingData:
    """
    Employee onboarding result.
    """

    employee_id: UUID

    onboarded: bool

    event_id: UUID | None = None


# ============================================================
# Workflow
# ============================================================


class EmployeeOnboardingWorkflow(
    BaseWorkflow[EmployeeOnboardingData],
):
    """
    Employee onboarding orchestration.
    """

    def __init__(
        self,
        *,
        request: EmployeeOnboardingRequest,
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
    ) -> WorkflowResult[EmployeeOnboardingData]:
        """
        Execute employee onboarding.
        """

        from apps.organization.employees.workflows import (
            EmployeeActivationRequest,
            EmployeeActivationWorkflow,
            EmployeeAssignmentRequest,
            EmployeeAssignmentWorkflow,
            EmployeeContractManagementRequest,
            EmployeeContractManagementWorkflow,
            EmployeeCreationRequest,
            EmployeeCreationWorkflow,
        )

        #
        # Step 1
        # Employee creation
        #
        creation_result = EmployeeCreationWorkflow(
            request=EmployeeCreationRequest(
                organization_id=(self._request.organization_id),
                **self._request.employee_data,
            ),
        ).execute(
            context=context,
        )

        employee_id = creation_result.data.employee_id

        #
        # Step 2
        # Contract setup
        #
        if self._request.contract_data:
            EmployeeContractManagementWorkflow(
                request=EmployeeContractManagementRequest(
                    employee_id=employee_id,
                    contract_data=(self._request.contract_data),
                ),
            ).execute(
                context=context,
            )

        #
        # Step 3
        # Organization assignment
        #
        if self._request.assignment_data:
            EmployeeAssignmentWorkflow(
                request=EmployeeAssignmentRequest(
                    employee_id=employee_id,
                    **self._request.assignment_data,
                ),
            ).execute(
                context=context,
            )

        #
        # Step 4
        # Activate employee
        #
        EmployeeActivationWorkflow(
            request=EmployeeActivationRequest(
                employee_id=employee_id,
            ),
        ).execute(
            context=context,
        )

        #
        # Domain event
        #
        event = EmployeeOnboardedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            employee_id=employee_id,
            organization_id=(self._request.organization_id),
        )

        self.publish_after_commit(
            event,
        )

        #
        # Background processing
        #
        self.dispatch_after_commit(
            send_employee_updated_notification,
            employee_id=employee_id,
        )

        self.dispatch_after_commit(
            index_employee,
            employee_id=employee_id,
        )

        self.dispatch_after_commit(
            synchronize_employee,
            employee_id=employee_id,
        )

        logger.info(
            "Employee onboarding completed.",
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
            data=EmployeeOnboardingData(
                employee_id=employee_id,
                onboarded=True,
                event_id=event.event_id,
            ),
            message=("Employee onboarded successfully."),
            code="employee_onboarded",
        )


__all__ = (
    "EmployeeOnboardingRequest",
    "EmployeeOnboardingData",
    "EmployeeOnboardingWorkflow",
)
