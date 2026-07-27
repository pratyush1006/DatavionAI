"""
Business services for salary structures.
"""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.hr.payroll.models import SalaryStructure

type SalaryStructureData = Mapping[str, object]


def _validate_salary_structure_data(
    *,
    validated_data: SalaryStructureData,
    instance: SalaryStructure | None = None,
) -> None:
    """
    Validate salary structure business rules.
    """

    employee = validated_data.get(
        "employee",
        instance.employee if instance else None,
    )

    organization = validated_data.get(
        "organization",
        instance.organization if instance else None,
    )

    effective_from = validated_data.get(
        "effective_from",
        instance.effective_from if instance else None,
    )

    effective_to = validated_data.get(
        "effective_to",
        instance.effective_to if instance else None,
    )

    if employee and organization and employee.organization_id != organization.id:
        raise ValidationError(
            "Employee must belong to the selected organization.",
        )

    if effective_to and effective_from and effective_to < effective_from:
        raise ValidationError(
            "Effective-to date must be on or after the effective-from date.",
        )

    queryset = SalaryStructure.objects.filter(
        employee=employee,
        effective_from=effective_from,
    )

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    if queryset.exists():
        raise ValidationError(
            "A salary structure already exists for this employee starting on this date.",
        )


@transaction.atomic
def create_salary_structure(
    *,
    validated_data: SalaryStructureData,
) -> SalaryStructure:
    """
    Create a new salary structure.
    """

    _validate_salary_structure_data(validated_data=validated_data)

    return SalaryStructure.objects.create(**validated_data)


@transaction.atomic
def update_salary_structure(
    *,
    instance: SalaryStructure,
    validated_data: SalaryStructureData,
) -> SalaryStructure:
    """
    Update an existing salary structure.
    """

    if not validated_data:
        return instance

    _validate_salary_structure_data(
        validated_data=validated_data,
        instance=instance,
    )

    for field, value in validated_data.items():
        setattr(instance, field, value)

    instance.save(update_fields=tuple(validated_data.keys()))

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_salary_structure(*, instance: SalaryStructure) -> None:
    """
    Delete a salary structure.
    """

    instance.delete()


__all__ = [
    "create_salary_structure",
    "update_salary_structure",
    "delete_salary_structure",
]
