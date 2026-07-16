"""
Business services for the Departments application.
"""

from __future__ import annotations

from collections.abc import Mapping

from apps.organization.departments.models import Department
from django.db import transaction

type DepartmentData = Mapping[str, object]


@transaction.atomic
def create_department(
    *,
    validated_data: DepartmentData,
) -> Department:
    """
    Create a department.
    """

    return Department.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_department(
    *,
    instance: Department,
    validated_data: DepartmentData,
) -> Department:
    """
    Update a department.
    """

    for field, value in validated_data.items():
        setattr(
            instance,
            field,
            value,
        )

    instance.save()

    instance.refresh_from_db()

    return instance


@transaction.atomic
def delete_department(
    *,
    instance: Department,
) -> None:
    """
    Delete a department.
    """

    instance.delete()


__all__ = [
    "create_department",
    "update_department",
    "delete_department",
]
