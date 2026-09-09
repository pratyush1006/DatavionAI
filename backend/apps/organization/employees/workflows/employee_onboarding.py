"""
Employee onboarding workflow.

Coordinates the complete employee onboarding lifecycle.

Responsibilities
----------------
- Validate tenant-scoped onboarding request
- Create employee identity
- Create optional employment contract
- Create optional organization assignment
- Activate employee
- Publish onboarding event
- Dispatch post-commit tasks

Architecture
------------

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

Important
---------
The onboarding workflow is the orchestration boundary.

Individual child workflows remain responsible for their respective
domain operations.

The parent workflow preserves child workflow failures rather than
converting them into generic runtime errors.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any
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
from django.db import transaction

logger = logging.getLogger(__name__)


# =============================================================================
# Request
# =============================================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeOnboardingRequest:
    """
    Complete employee onboarding request.

    Parameters
    ----------
    organization_id:
        Organization receiving the employee.

    employee_data:
        Employee creation payload.

    contract_data:
        Optional employment contract payload.

    assignment_data:
        Optional organization assignment payload.
    """

    organization_id: UUID

    employee_data: dict[str, Any]

    contract_data: dict[str, Any] | None = None

    assignment_data: dict[str, Any] | None = None


# =============================================================================
# Result
# =============================================================================


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


# =============================================================================
# Workflow
# =============================================================================


class EmployeeOnboardingWorkflow(
    BaseWorkflow[EmployeeOnboardingData],
):
    """
    Orchestrate the complete employee onboarding lifecycle.

    Workflow:

        Actor
          |
          v
        Employee Creation
          |
          v
        Contract Setup
          |
          v
        Assignment Setup
          |
          v
        Activation
          |
          v
        Onboarding Event
          |
          v
        Background Tasks

    All database changes are protected by one transaction.

    Child workflow failures are returned unchanged so that:

    - domain error codes are preserved
    - authorization failures remain failures
    - API error mapping remains accurate
    - diagnostics are not lost
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

    # =========================================================================
    # Child workflow failure propagation
    # =========================================================================

    @staticmethod
    def _propagate_failure(
        result: WorkflowResult[Any],
    ) -> WorkflowResult[Any] | None:
        """
        Return a failed child result when the child workflow failed.

        Successful results return None.

        This prevents the orchestration layer from replacing meaningful
        workflow/domain errors with generic RuntimeError instances.
        """

        if result.success:
            return None

        return WorkflowResult.fail(
            context=result.context,
            message=(result.message or "Employee onboarding step failed."),
            code=(result.code or "employee_onboarding_step_failed"),
            error=result.error,
            metadata={
                **result.metadata,
                "onboarding_workflow": ("employee.onboard"),
                "child_workflow": (result.context.workflow_name),
            },
            duration_ms=result.duration_ms,
        )

    # =========================================================================
    # Execution
    # =========================================================================

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[EmployeeOnboardingData]:
        """
        Execute complete employee onboarding.

        The database transaction covers the complete orchestration.

        If any child workflow fails, the transaction is rolled back and
        the original workflow failure is preserved.
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
        from apps.platform.organizations.models import Organization

        # ---------------------------------------------------------------------
        # Step 0
        # Resolve organization inside tenant boundary
        # ---------------------------------------------------------------------

        organization = Organization.objects.get(
            id=self._request.organization_id,
            tenant_id=context.tenant_id,
        )

        # ---------------------------------------------------------------------
        # Step 1
        # Employee creation
        # ---------------------------------------------------------------------

        creation_result = EmployeeCreationWorkflow(
            request=EmployeeCreationRequest(
                organization_id=organization.id,
                **self._request.employee_data,
            ),
        ).execute(
            context=context,
        )

        creation_failure = self._propagate_failure(
            creation_result,
        )

        if creation_failure is not None:
            return creation_failure

        if creation_result.data is None:
            return WorkflowResult.fail(
                context=context,
                message=(
                    "Employee creation workflow completed "
                    "without returning employee data."
                ),
                code="employee_creation_missing_data",
            )

        employee_id = creation_result.data.employee_id

        # ---------------------------------------------------------------------
        # Step 2
        # Contract setup
        # ---------------------------------------------------------------------

        if self._request.contract_data:
            contract_result = EmployeeContractManagementWorkflow(
                request=(
                    EmployeeContractManagementRequest(
                        employee_id=employee_id,
                        contract_data=(self._request.contract_data),
                    )
                ),
            ).execute(
                context=context,
            )

            contract_failure = self._propagate_failure(
                contract_result,
            )

            if contract_failure is not None:
                return contract_failure

            if contract_result.data is None:
                return WorkflowResult.fail(
                    context=context,
                    message=(
                        "Employee contract workflow completed "
                        "without returning contract data."
                    ),
                    code="employee_contract_missing_data",
                )

        # ---------------------------------------------------------------------
        # Step 3
        # Organization assignment
        # ---------------------------------------------------------------------

        if self._request.assignment_data:
            assignment_result = EmployeeAssignmentWorkflow(
                request=EmployeeAssignmentRequest(
                    employee_id=employee_id,
                    **self._request.assignment_data,
                ),
            ).execute(
                context=context,
            )

            assignment_failure = self._propagate_failure(
                assignment_result,
            )

            if assignment_failure is not None:
                return assignment_failure

            if assignment_result.data is None:
                return WorkflowResult.fail(
                    context=context,
                    message=(
                        "Employee assignment workflow completed "
                        "without returning assignment data."
                    ),
                    code="employee_assignment_missing_data",
                )

        # ---------------------------------------------------------------------
        # Step 4
        # Activate employee
        # ---------------------------------------------------------------------

        activation_result = EmployeeActivationWorkflow(
            request=EmployeeActivationRequest(
                employee_id=employee_id,
            ),
        ).execute(
            context=context,
        )

        activation_failure = self._propagate_failure(
            activation_result,
        )

        if activation_failure is not None:
            return activation_failure

        if activation_result.data is None:
            return WorkflowResult.fail(
                context=context,
                message=(
                    "Employee activation workflow completed "
                    "without returning activation data."
                ),
                code="employee_activation_missing_data",
            )

        # ---------------------------------------------------------------------
        # Step 5
        # Employee onboarded event
        # ---------------------------------------------------------------------

        event = EmployeeOnboardedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            employee_id=employee_id,
            organization_id=organization.id,
        )

        #
        # The event must only become visible after the transaction commits.
        #
        self.publish_after_commit(
            event,
        )

        # ---------------------------------------------------------------------
        # Step 6
        # Post-commit background processing
        # ---------------------------------------------------------------------

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

        # ---------------------------------------------------------------------
        # Logging
        # ---------------------------------------------------------------------

        self._logger.info(
            "Employee onboarding completed.",
            extra={
                "employee_id": str(employee_id),
                "organization_id": str(
                    organization.id,
                ),
                "tenant_id": str(
                    context.tenant_id,
                ),
                "actor_id": str(
                    context.actor_id,
                ),
                "workflow": "employee.onboard",
            },
        )

        # ---------------------------------------------------------------------
        # Result
        # ---------------------------------------------------------------------

        return WorkflowResult.ok(
            context=context,
            data=EmployeeOnboardingData(
                employee_id=employee_id,
                onboarded=True,
                event_id=event.event_id,
            ),
            message="Employee onboarded successfully.",
            code="employee_onboarded",
        )


__all__ = (
    "EmployeeOnboardingRequest",
    "EmployeeOnboardingData",
    "EmployeeOnboardingWorkflow",
)
