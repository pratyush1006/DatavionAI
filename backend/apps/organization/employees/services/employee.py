"""
Business services for the Employees app.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.organization.employees.models import Employee

type EmployeeData = Mapping[str, object]


def _validate_employee_data(
    *,
    validated_data: EmployeeData,
    instance: Employee | None = None,
) -> None:
    """
    Validate employee business rules.
    """

    organization = validated_data.get(
        "organization",
        instance.organization if instance else None,
    )

    department = validated_data.get(
        "department",
        instance.department if instance else None,
    )

    team = validated_data.get(
        "team",
        instance.team if instance else None,
    )

    manager = validated_data.get(
        "manager",
        instance.manager if instance else None,
    )

    user = validated_data.get(
        "user",
        instance.user if instance else None,
    )

    employee_code = validated_data.get(
        "employee_code",
        instance.employee_code if instance else None,
    )

    if organization and department and department.organization_id != organization.id:
        raise ValidationError(
            "Selected department does not belong to the selected organization.",
        )

    if team and department and team.department_id != department.id:
        raise ValidationError(
            "Selected team does not belong to the selected department.",
        )

    if manager and organization and manager.organization_id != organization.id:
        raise ValidationError(
            "Manager must belong to the selected organization.",
        )

    if (
        user
        and organization
        and hasattr(user, "organization_id")
        and user.organization_id != organization.id
    ):
        raise ValidationError(
            "User must belong to the selected organization.",
        )

    queryset = Employee.objects.filter(
        organization=organization,
        employee_code=employee_code,
    )

    if instance:
        queryset = queryset.exclude(
            pk=instance.pk,
        )

    if queryset.exists():
        raise ValidationError(
            "Employee code already exists in this organization.",
        )


@transaction.atomic
def create_employee(
    *,
    validated_data: EmployeeData,
) -> Employee:
    """
    Create a new employee.
    """

    _validate_employee_data(
        validated_data=validated_data,
    )

    return Employee.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_employee(
    *,
    instance: Employee,
    validated_data: EmployeeData,
) -> Employee:
    """
    Update an existing employee.
    """

    if not validated_data:
        return instance

    _validate_employee_data(
        validated_data=validated_data,
        instance=instance,
    )

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save(
        update_fields=tuple(validated_data.keys()),
    )

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_employee(
    *,
    instance: Employee,
) -> None:
    """
    Delete an employee.
    """

    instance.delete()
