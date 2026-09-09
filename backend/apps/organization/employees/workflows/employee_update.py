"""
Employee update workflow.

Coordinates employee aggregate updates.

Responsibilities
----------------
- Tenant-scoped employee lookup
- RBAC authorization
- Enforce workflow-level update boundaries
- Delegate employee mutation to the domain service
- Publish employee lifecycle events
- Dispatch post-commit background tasks

Non-responsibilities
--------------------
- API serialization
- API-specific validation
- Employee domain validation
- Direct model mutation
- Notifications
- Search/index implementation
- Synchronization implementation
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
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
from django.core.exceptions import ValidationError
from django.db import transaction

logger = logging.getLogger(__name__)


# =============================================================================
# Workflow Contract
# =============================================================================

type EmployeeUpdateDataMap = Mapping[str, object]


# Fields intentionally exposed by EmployeeUpdateSerializer and therefore
# allowed through this workflow.
#
# Immutable employee identity/lifecycle fields such as:
#
# - id
# - organization
# - employee_code
# - joining_date
# - status
#
# are deliberately excluded.
#
# This is a workflow-level safety boundary for callers that do not originate
# from the DRF serializer layer.
_ALLOWED_UPDATE_FIELDS = frozenset(
    {
        "designation",
        "work_email",
        "phone_number",
        "employment_type",
        "confirmation_date",
        "metadata",
    },
)


# =============================================================================
# Request
# =============================================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeUpdateRequest:
    """
    Employee update request.

    The payload normally originates from EmployeeUpdateSerializer,
    but the workflow defensively enforces its own mutable-field
    boundary so that non-API callers cannot update protected fields.
    """

    employee_id: UUID

    data: EmployeeUpdateDataMap


# =============================================================================
# Result
# =============================================================================


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EmployeeUpdateData:
    """
    Result of employee update.
    """

    employee_id: UUID

    updated: bool

    event_id: UUID | None = None


# =============================================================================
# Workflow
# =============================================================================


class EmployeeUpdateWorkflow(
    BaseWorkflow[EmployeeUpdateData],
):
    """
    Update an employee aggregate.

    Workflow:

        Actor
          |
          v
        Tenant-scoped Employee Lookup
          |
          v
        RBAC Policy
          |
          v
        Update Boundary Validation
          |
          v
        Employee Domain Service
          |
          v
        Domain Event
          |
          v
        Post-Commit Tasks

    The workflow owns orchestration and application-level boundaries.

    Employee business invariants and persistence remain inside the
    employee domain service.

    Events and background tasks are registered only after the domain
    mutation succeeds and are executed after the surrounding transaction
    commits successfully.
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

    def _validate_update_fields(
        self,
    ) -> None:
        """
        Ensure only workflow-approved employee fields are updated.

        API serializers normally enforce this boundary. The workflow
        repeats the boundary because workflows may also be invoked by
        non-HTTP callers such as background jobs, internal services, or
        future integrations.

        Unknown or protected fields are rejected rather than silently
        discarded.
        """

        invalid_fields = frozenset(self._request.data).difference(
            _ALLOWED_UPDATE_FIELDS,
        )

        if invalid_fields:
            fields = ", ".join(
                sorted(
                    invalid_fields,
                ),
            )

            raise ValidationError(
                f"Employee update contains unsupported fields: {fields}.",
            )

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[EmployeeUpdateData]:
        """
        Execute employee update.

        The workflow transaction encompasses:

        - Actor resolution
        - Tenant-scoped employee resolution
        - Authorization
        - Employee domain mutation
        - Domain event registration
        - Background task registration

        This ensures post-commit callbacks cannot execute before the
        complete workflow transaction has successfully committed.
        """

        self._validate_update_fields()

        if not self._request.data:
            return WorkflowResult.ok(
                context=context,
                data=EmployeeUpdateData(
                    employee_id=self._request.employee_id,
                    updated=False,
                ),
                message="No employee changes were requested.",
                code="employee_update_no_changes",
            )

        from apps.platform.accounts.models import User

        with transaction.atomic():
            actor = User.objects.get(
                id=context.actor_id,
            )

            employee = Employee.objects.select_related(
                "organization",
            ).get(
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

            employee = update_employee(
                instance=employee,
                validated_data=self._request.data,
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
                "event_id": str(
                    event.event_id,
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
            message="Employee updated successfully.",
            code="employee_updated",
        )


__all__: tuple[str, ...] = (
    "EmployeeUpdateData",
    "EmployeeUpdateRequest",
    "EmployeeUpdateWorkflow",
)
