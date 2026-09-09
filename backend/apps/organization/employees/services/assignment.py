"""
Employee assignment domain service.

Responsibilities
----------------
- Create employee assignments
- Close previous assignments
- Maintain current assignment
- Validate organization boundaries
- Maintain assignment date invariants
- Protect current-assignment concurrency

Non-responsibilities
--------------------
- RBAC
- Notifications
- Events
- Workflow orchestration

The service is intentionally independent from API and workflow layers.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from apps.organization.employees.models import (
    Employee,
    EmployeeAssignment,
)
from django.core.exceptions import ValidationError
from django.db import transaction


@transaction.atomic
def change_employee_assignment(
    *,
    employee: Employee,
    department: Any,
    team: Any = None,
    supervisor: Employee | None = None,
    effective_from: date,
) -> EmployeeAssignment:
    """
    Change an employee's organizational assignment.

    Lifecycle
    ---------
    1. Validate the effective date.
    2. Validate department ownership.
    3. Validate team ownership and department relationship.
    4. Validate supervisor ownership.
    5. Lock the current assignment.
    6. Close the current assignment one day before the
       new assignment begins.
    7. Create the new current assignment.

    The operation is transactional so a failure cannot leave
    the employee without a valid current assignment.
    """

    if not isinstance(
        effective_from,
        date,
    ):
        raise ValidationError(
            "Effective from must be a valid date.",
        )

    #
    # Department must belong to the employee organization.
    #
    if department.organization_id != employee.organization_id:
        raise ValidationError(
            "Department does not belong to employee organization.",
        )

    #
    # Team validation.
    #
    if team is not None:
        if team.department_id != department.id:
            raise ValidationError(
                "Team does not belong to the selected department.",
            )

        team_organization_id = getattr(
            team,
            "organization_id",
            None,
        )

        if (
            team_organization_id is not None
            and team_organization_id != employee.organization_id
        ):
            raise ValidationError(
                "Team does not belong to employee organization.",
            )

    #
    # Supervisor validation.
    #
    if supervisor is not None:
        if supervisor.organization_id != employee.organization_id:
            raise ValidationError(
                "Supervisor must belong to employee organization.",
            )

        if supervisor.id == employee.id:
            raise ValidationError(
                "Employee cannot supervise themselves.",
            )

    #
    # Lock the current assignment.
    #
    current_assignment = (
        EmployeeAssignment.objects.select_for_update()
        .filter(
            employee=employee,
            is_current=True,
        )
        .first()
    )

    #
    # If an existing current assignment exists, the new
    # assignment must begin after it.
    #
    if current_assignment is not None:
        if effective_from <= current_assignment.effective_from:
            raise ValidationError(
                "New assignment effective date must be after "
                "the current assignment effective date.",
            )

        historical_effective_to = effective_from - timedelta(days=1)

        if historical_effective_to < current_assignment.effective_from:
            raise ValidationError(
                "New assignment would create an invalid assignment history.",
            )

        current_assignment.is_current = False
        current_assignment.effective_to = historical_effective_to

        current_assignment.save(
            update_fields=(
                "is_current",
                "effective_to",
                "updated_at",
            ),
        )

    #
    # Create the new current assignment.
    #
    assignment = EmployeeAssignment.objects.create(
        employee=employee,
        department=department,
        team=team,
        supervisor=supervisor,
        effective_from=effective_from,
        effective_to=None,
        is_current=True,
    )

    return assignment


__all__ = ("change_employee_assignment",)
