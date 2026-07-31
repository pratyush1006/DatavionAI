"""
Employee domain services.

Responsibilities:

- Employee creation
- Employee updates
- Employee deletion
- Employee validation

Non-responsibilities:

- Department assignment
- Team assignment
- Contract management
- Workflow execution
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.organization.employees.models import (
    Employee,
)

type EmployeeData = Mapping[str, object]


# ============================================================
# Validation
# ============================================================


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

    user = validated_data.get(
        "user",
        instance.user if instance else None,
    )

    employee_code = validated_data.get(
        "employee_code",
        instance.employee_code if instance else None,
    )

    #
    # User organization validation
    #
    if (
        user
        and organization
        and hasattr(
            user,
            "organization_id",
        )
        and user.organization_id
        and user.organization_id != organization.id
    ):
        raise ValidationError(
            "User must belong to the selected organization.",
        )

    #
    # Organization employee code uniqueness
    #
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


# ============================================================
# Create
# ============================================================


@transaction.atomic
def create_employee(
    *,
    validated_data: EmployeeData,
) -> Employee:
    """
    Create employee.
    """

    _validate_employee_data(
        validated_data=validated_data,
    )

    return Employee.objects.create(
        **validated_data,
    )


# ============================================================
# Update
# ============================================================


@transaction.atomic
def update_employee(
    *,
    instance: Employee,
    validated_data: EmployeeData,
) -> Employee:
    """
    Update employee.
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
        update_fields=tuple(
            validated_data.keys(),
        ),
    )

    instance.refresh_from_db()

    return instance


# ============================================================
# Delete
# ============================================================


@transaction.atomic
def delete_employee(
    *,
    instance: Employee,
) -> None:
    """
    Soft delete employee.
    """

    instance.delete()


__all__ = (
    "create_employee",
    "update_employee",
    "delete_employee",
)
