from django.shortcuts import get_object_or_404

from apps.employees.models import Employee


def get_employees():
    """
    Return all employees.
    """

    return Employee.objects.select_related(
        "user",
        "organization",
        "department",
        "team",
        "manager",
        "manager__user",
    )


def get_employee_by_id(
    employee_id: int,
) -> Employee:
    """
    Return an employee by ID.
    """

    return get_object_or_404(
        Employee.objects.select_related(
            "user",
            "organization",
            "department",
            "team",
            "manager",
            "manager__user",
        ),
        id=employee_id,
    )
