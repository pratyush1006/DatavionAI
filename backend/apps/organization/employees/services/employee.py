"""
Employee domain services.

Responsibilities
----------------
- Employee creation
- Employee updates
- Employee deletion
- Employee business validation

Non-responsibilities
--------------------
- Department assignment
- Team assignment
- Contract management
- RBAC
- Events
- Notifications
- Workflow orchestration

The service operates on the Employee aggregate root and is
independent from API and workflow layers.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.organization.employees.constants import (
    DEFAULT_EMPLOYMENT_STATUS,
    DEFAULT_EMPLOYMENT_TYPE,
)
from apps.organization.employees.models import (
    Employee,
)
from django.core.exceptions import ValidationError
from django.db import transaction

type EmployeeData = Mapping[str, object]


# ==============================================================================
# Validation
# ==============================================================================


def _validate_employee_data(
    *,
    validated_data: EmployeeData,
    instance: Employee | None = None,
) -> None:
    """
    Validate employee domain invariants.

    Validation performed here is intentionally limited to rules
    belonging to the Employee aggregate.

    API-specific validation belongs in serializers.

    Authorization belongs in policies.

    Cross-aggregate lifecycle orchestration belongs in workflows.
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

    designation = validated_data.get(
        "designation",
        instance.designation if instance else None,
    )

    joining_date = validated_data.get(
        "joining_date",
        instance.joining_date if instance else None,
    )

    confirmation_date = validated_data.get(
        "confirmation_date",
        instance.confirmation_date if instance else None,
    )

    termination_date = validated_data.get(
        "termination_date",
        instance.termination_date if instance else None,
    )

    manager = validated_data.get(
        "manager",
        instance.manager if instance else None,
    )

    if organization is None:
        raise ValidationError(
            "Employee organization is required.",
        )

    if not employee_code:
        raise ValidationError(
            "Employee code is required.",
        )

    if not designation:
        raise ValidationError(
            "Employee designation is required.",
        )

    if joining_date is None:
        raise ValidationError(
            "Employee joining date is required.",
        )

    # ------------------------------------------------------------------
    # User organization boundary
    # ------------------------------------------------------------------

    if user is not None:
        user_organization_id = getattr(
            user,
            "organization_id",
            None,
        )

        if user_organization_id and user_organization_id != organization.id:
            raise ValidationError(
                "User must belong to the selected organization.",
            )

    # ------------------------------------------------------------------
    # Manager validation
    # ------------------------------------------------------------------

    if manager is not None:
        if manager.id == (instance.id if instance is not None else None):
            raise ValidationError(
                "Employee cannot be their own manager.",
            )

        if manager.organization_id != organization.id:
            raise ValidationError(
                "Manager must belong to the employee organization.",
            )

    # ------------------------------------------------------------------
    # Employment dates
    # ------------------------------------------------------------------

    if confirmation_date is not None and confirmation_date < joining_date:
        raise ValidationError(
            "Confirmation date cannot be before joining date.",
        )

    if termination_date is not None and termination_date < joining_date:
        raise ValidationError(
            "Termination date cannot be before joining date.",
        )

    if (
        termination_date is not None
        and confirmation_date is not None
        and termination_date < confirmation_date
    ):
        raise ValidationError(
            "Termination date cannot be before confirmation date.",
        )

    # ------------------------------------------------------------------
    # Employee code uniqueness
    # ------------------------------------------------------------------

    queryset = Employee.objects.filter(
        organization=organization,
        employee_code=employee_code,
    )

    if instance is not None:
        queryset = queryset.exclude(
            pk=instance.pk,
        )

    if queryset.exists():
        raise ValidationError(
            "Employee code already exists in this organization.",
        )


# ==============================================================================
# Normalization
# ==============================================================================


def _normalize_employee_data(
    *,
    validated_data: EmployeeData,
    instance: Employee | None = None,
) -> dict[str, Any]:
    """
    Normalize employee persistence data.

    Defaults are applied at the service boundary so callers that
    bypass the serializer still receive domain-safe values.
    """

    data = dict(validated_data)

    # ------------------------------------------------------------------
    # Employee code
    # ------------------------------------------------------------------

    if "employee_code" in data:
        employee_code = data["employee_code"]

        if isinstance(employee_code, str):
            data["employee_code"] = employee_code.strip().upper()

    elif instance is None:
        raise ValidationError(
            "Employee code is required.",
        )

    # ------------------------------------------------------------------
    # Designation
    # ------------------------------------------------------------------

    if "designation" in data:
        designation = data["designation"]

        if isinstance(designation, str):
            data["designation"] = designation.strip()

    # ------------------------------------------------------------------
    # Work email
    # ------------------------------------------------------------------

    if "work_email" in data:
        work_email = data["work_email"]

        if isinstance(work_email, str):
            data["work_email"] = work_email.strip().lower()

    # ------------------------------------------------------------------
    # Phone number
    # ------------------------------------------------------------------

    if "phone_number" in data:
        phone_number = data["phone_number"]

        if isinstance(phone_number, str):
            data["phone_number"] = phone_number.strip()

    # ------------------------------------------------------------------
    # Employment type
    # ------------------------------------------------------------------

    if "employment_type" not in data and instance is None:
        data["employment_type"] = DEFAULT_EMPLOYMENT_TYPE

    # ------------------------------------------------------------------
    # Employment status
    # ------------------------------------------------------------------

    if "status" not in data and instance is None:
        data["status"] = DEFAULT_EMPLOYMENT_STATUS

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    if "metadata" in data and data["metadata"] is None:
        data["metadata"] = {}

    return data


# ==============================================================================
# Create
# ==============================================================================


@transaction.atomic
def create_employee(
    *,
    validated_data: EmployeeData,
) -> Employee:
    """
    Create an Employee aggregate.

    The operation is transactional and validates the aggregate
    before persistence.

    Returns
    -------
    Employee
        Persisted employee instance.
    """

    data = _normalize_employee_data(
        validated_data=validated_data,
    )

    _validate_employee_data(
        validated_data=data,
    )

    return Employee.objects.create(
        **data,
    )


# ==============================================================================
# Update
# ==============================================================================


@transaction.atomic
def update_employee(
    *,
    instance: Employee,
    validated_data: EmployeeData,
) -> Employee:
    """
    Update an Employee aggregate.

    Only supplied fields are modified.

    Aggregate invariants are validated against the resulting
    employee state before persistence.
    """

    if not validated_data:
        return instance

    data = _normalize_employee_data(
        validated_data=validated_data,
        instance=instance,
    )

    _validate_employee_data(
        validated_data=data,
        instance=instance,
    )

    changed_fields: list[str] = []

    for field, value in data.items():
        if not hasattr(instance, field):
            raise ValidationError(
                f"Unknown employee field: {field}.",
            )

        if getattr(instance, field) != value:
            setattr(
                instance,
                field,
                value,
            )
            changed_fields.append(field)

    if not changed_fields:
        return instance

    instance.save(
        update_fields=tuple(
            changed_fields,
        ),
    )

    instance.refresh_from_db()

    return instance


# ==============================================================================
# Delete
# ==============================================================================


@transaction.atomic
def delete_employee(
    *,
    instance: Employee,
) -> None:
    """
    Delete an employee through the model's configured lifecycle.

    Employee inherits SoftDeleteModel through BaseModel, so the
    model's delete implementation determines whether this becomes
    a soft deletion.
    """

    instance.delete()


# ==============================================================================
# Public API
# ==============================================================================


__all__ = (
    "create_employee",
    "update_employee",
    "delete_employee",
)
