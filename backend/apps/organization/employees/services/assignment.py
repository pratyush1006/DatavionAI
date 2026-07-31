"""
Employee assignment domain service.

Responsibilities:

- Create employee assignments
- Close previous assignments
- Maintain current assignment
- Validate organization boundaries

Non-responsibilities:

- RBAC
- Notifications
- Events
- Workflow orchestration
"""

from __future__ import annotations

from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.organization.employees.models import (
    Employee,
    EmployeeAssignment,
)


@transaction.atomic
def change_employee_assignment(
    *,
    employee: Employee,
    department,
    team=None,
    supervisor=None,
    effective_from: date,
) -> EmployeeAssignment:
    """
    Change employee organizational assignment.

    Process:

    1. Validate relationships
    2. Close existing assignment
    3. Create new current assignment
    """

    #
    # Department belongs to employee organization
    #
    if department.organization_id != employee.organization_id:
        raise ValidationError(
            "Department does not belong to employee organization.",
        )

    #
    # Supervisor validation
    #
    if supervisor:
        if supervisor.organization_id != employee.organization_id:
            raise ValidationError(
                "Supervisor must belong to employee organization.",
            )

        if supervisor.id == employee.id:
            raise ValidationError(
                "Employee cannot supervise themselves.",
            )

    #
    # Close current assignment
    #
    EmployeeAssignment.objects.filter(
        employee=employee,
        is_current=True,
    ).update(
        is_current=False,
        effective_to=effective_from,
    )

    #
    # Create new assignment
    #
    assignment = EmployeeAssignment.objects.create(
        employee=employee,
        department=department,
        team=team,
        supervisor=supervisor,
        effective_from=effective_from,
        is_current=True,
    )

    return assignment


__all__ = ("change_employee_assignment",)
