from django.core.exceptions import ValidationError

from apps.employees.models import Employee


def _validate_employee_data(
    validated_data: dict,
    employee: Employee | None = None,
) -> None:
    """
    Validate employee business rules.
    """

    organization = validated_data.get(
        "organization",
        employee.organization if employee else None,
    )

    department = validated_data.get(
        "department",
        employee.department if employee else None,
    )

    team = validated_data.get(
        "team",
        employee.team if employee else None,
    )

    manager = validated_data.get(
        "manager",
        employee.manager if employee else None,
    )

    user = validated_data.get(
        "user",
        employee.user if employee else None,
    )

    employee_code = validated_data.get(
        "employee_code",
        employee.employee_code if employee else None,
    )

    # Department must belong to Organization
    if organization and department and department.organization_id != organization.id:
        raise ValidationError(
            "Selected department does not belong to the selected organization."
        )

    # Team must belong to Department
    if team and department and team.department_id != department.id:
        raise ValidationError(
            "Selected team does not belong to the selected department."
        )

    # Manager must belong to same Organization
    if manager and organization and manager.organization_id != organization.id:
        raise ValidationError("Manager must belong to the selected organization.")

    # User must belong to same Organization
    if user and organization and user.organization_id != organization.id:
        raise ValidationError("User must belong to the selected organization.")

    # Prevent duplicate employee code
    queryset = Employee.objects.filter(
        organization=organization,
        employee_code=employee_code,
    )

    if employee:
        queryset = queryset.exclude(
            pk=employee.pk,
        )

    if queryset.exists():
        raise ValidationError("Employee code already exists in this organization.")


def create_employee(
    validated_data: dict,
) -> Employee:
    """
    Create a new employee.
    """

    _validate_employee_data(validated_data)

    return Employee.objects.create(**validated_data)


def update_employee(
    employee: Employee,
    validated_data: dict,
) -> Employee:
    """
    Update an existing employee.
    """

    _validate_employee_data(
        validated_data,
        employee,
    )

    for field, value in validated_data.items():
        setattr(
            employee,
            field,
            value,
        )

    employee.save()

    return employee


def delete_employee(
    employee: Employee,
) -> None:
    """
    Delete an existing employee.
    """

    employee.delete()
