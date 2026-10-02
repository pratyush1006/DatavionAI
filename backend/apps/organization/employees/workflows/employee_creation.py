"""
Employee creation workflow.

Coordinates the complete employee creation lifecycle.

Responsibilities
----------------
- Resolve actor
- Resolve tenant-scoped organization
- Validate RBAC policy
- Resolve optional linked user
- Execute employee domain service
- Publish employee-created domain event
- Dispatch post-commit background tasks

Non-responsibilities
--------------------
- Business validation
- Persistence implementation
- RBAC implementation
- Event publishing implementation
- Background task implementation

Architecture
------------

Workflow
 |
 +--> Actor / Tenant Resolution
 |
 +--> EmployeePolicy
 |
 +--> Employee Service
 |
 +--> EmployeeCreatedEvent
 |
 +--> Post-Commit Tasks

Design
------
The workflow is the application orchestration boundary.

Domain validation remains inside the employee service.
Authorization remains inside the employee policy.
Persistence remains inside the domain service.
Events and asynchronous side effects are registered after
successful transaction commit.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from typing import Any
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.core.workflows.exceptions import (
    WorkflowError,
)
from apps.organization.employees.constants import (
    DEFAULT_EMPLOYMENT_STATUS,
    DEFAULT_EMPLOYMENT_TYPE,
    EmploymentStatus,
    EmploymentType,
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
from django.core.exceptions import ObjectDoesNotExist
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
class EmployeeCreationRequest:
    """
    Employee creation request.

    Organization and user are supplied as UUID references and are
    resolved inside the workflow so tenant and organization boundaries
    can be enforced before persistence.
    """

    organization_id: UUID

    employee_code: str

    designation: str

    joining_date: date

    user_id: UUID | None = None

    work_email: str | None = None

    phone_number: str | None = None

    employment_type: EmploymentType | str | None = None

    status: EmploymentStatus | str | None = None


# =============================================================================
# Result
# =============================================================================


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


# =============================================================================
# Workflow
# =============================================================================


class EmployeeCreationWorkflow(
    BaseWorkflow[EmployeeCreationData],
):
    """
    Create an employee inside the current tenant.

    Flow
    ----

        Actor
          |
          v
        Tenant-scoped Organization Lookup
          |
          v
        RBAC Policy
          |
          v
        Optional User Resolution
          |
          v
        Employee Domain Service
          |
          v
        EmployeeCreatedEvent
          |
          v
        Post-Commit Tasks

    The workflow never performs direct employee persistence.
    """

    def __init__(
        self,
        *,
        request: EmployeeCreationRequest,
        policy: EmployeePolicy | None = None,
        logger_: logging.Logger | None = None,
    ) -> None:
        super().__init__(
            logger_=logger_,
        )

        self._request = request

        self._policy = policy or EmployeePolicy()

    # =========================================================================
    # Error helpers
    # =========================================================================

    @staticmethod
    def _failure(
        *,
        context: WorkflowContext,
        message: str,
        code: str,
        error: WorkflowError | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> WorkflowResult[EmployeeCreationData]:
        """
        Build a standardized failed workflow result.
        """

        return WorkflowResult.fail(
            context=context,
            message=message,
            code=code,
            error=error,
            metadata=metadata or {},
        )

    # =========================================================================
    # Execution
    # =========================================================================

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[EmployeeCreationData]:
        """
        Execute employee creation.

        The aggregate creation and registration of post-commit
        side effects are performed within the same database
        transaction boundary.
        """

        from apps.platform.accounts.models import User
        from apps.platform.organizations.models import Organization

        # ---------------------------------------------------------------------
        # Step 1
        # Resolve actor
        # ---------------------------------------------------------------------

        try:
            actor = User.objects.get(
                id=context.actor_id,
            )
        except ObjectDoesNotExist:
            return self._failure(
                context=context,
                message="Workflow actor could not be resolved.",
                code="employee_actor_not_found",
                metadata={
                    "actor_id": str(
                        context.actor_id,
                    ),
                },
            )

        # ---------------------------------------------------------------------
        # Step 2
        # Resolve tenant-scoped organization
        # ---------------------------------------------------------------------

        try:
            organization = Organization.objects.get(
                id=self._request.organization_id,
                tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist:
            return self._failure(
                context=context,
                message=("Organization does not exist within the current tenant."),
                code="employee_organization_not_found",
                metadata={
                    "organization_id": str(
                        self._request.organization_id,
                    ),
                    "tenant_id": str(
                        context.tenant_id,
                    ),
                },
            )

        # ---------------------------------------------------------------------
        # Step 3
        # Authorization
        # ---------------------------------------------------------------------

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            return self._failure(
                context=context,
                message=("User does not have permission to create employee."),
                code="employee_create_forbidden",
                metadata={
                    "organization_id": str(
                        organization.id,
                    ),
                    "actor_id": str(
                        context.actor_id,
                    ),
                },
            )

        # ---------------------------------------------------------------------
        # Step 4
        # Resolve optional linked user
        # ---------------------------------------------------------------------

        user = None

        if self._request.user_id is not None:
            try:
                user = User.objects.get(
                    id=self._request.user_id,
                    organization_id=organization.id,
                )
            except ObjectDoesNotExist:
                return self._failure(
                    context=context,
                    message=(
                        "Linked user does not exist within the selected organization."
                    ),
                    code="employee_user_not_found",
                    metadata={
                        "user_id": str(
                            self._request.user_id,
                        ),
                        "organization_id": str(
                            organization.id,
                        ),
                    },
                )

        # ---------------------------------------------------------------------
        # Step 5
        # Resolve lifecycle defaults
        # ---------------------------------------------------------------------

        employment_type = self._request.employment_type or DEFAULT_EMPLOYMENT_TYPE

        status = self._request.status or DEFAULT_EMPLOYMENT_STATUS

        # ---------------------------------------------------------------------
        # Step 6
        # Create employee through domain service
        # ---------------------------------------------------------------------

        employee = create_employee(
            validated_data={
                "organization": organization,
                "user": user,
                "employee_code": (self._request.employee_code),
                "designation": (self._request.designation),
                "work_email": (self._request.work_email),
                "phone_number": (self._request.phone_number),
                "employment_type": employment_type,
                "status": status,
                "joining_date": (self._request.joining_date),
            },
        )

        # ---------------------------------------------------------------------
        # Step 7
        # Domain event
        # ---------------------------------------------------------------------

        event = EmployeeCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            employee_id=employee.id,
            organization_id=organization.id,
        )

        #
        # Domain events must not be visible before the database
        # transaction successfully commits.
        #
        self.publish_after_commit(
            event,
        )

        # ---------------------------------------------------------------------
        # Step 8
        # Post-commit processing
        # ---------------------------------------------------------------------

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

        # ---------------------------------------------------------------------
        # Step 9
        # Logging
        # ---------------------------------------------------------------------

        self._logger.info(
            "Employee created.",
            extra={
                "workflow": "employee.create",
                "employee_id": str(
                    employee.id,
                ),
                "organization_id": str(
                    organization.id,
                ),
                "tenant_id": str(
                    context.tenant_id,
                ),
                "actor_id": str(
                    context.actor_id,
                ),
                "employee_code": (employee.employee_code),
                "status": employee.status,
            },
        )

        # ---------------------------------------------------------------------
        # Step 10
        # Result
        # ---------------------------------------------------------------------

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


# =============================================================================
# Public API
# =============================================================================


__all__ = (
    "EmployeeCreationRequest",
    "EmployeeCreationData",
    "EmployeeCreationWorkflow",
)
