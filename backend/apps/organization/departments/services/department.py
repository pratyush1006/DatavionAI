"""
Business services for the Departments application.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.organization.departments.models import Department
from apps.platform.accounts.models import User
from django.db import transaction

type DepartmentData = Mapping[str, Any]


class DepartmentService:
    """
    Business services for Department.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: DepartmentData,
    ) -> Department:
        """
        Create a department.
        """

        department = Department(
            **validated_data,
        )

        department.full_clean()

        department.save()

        return department

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Department,
        validated_data: DepartmentData,
    ) -> Department:
        """
        Update a department.
        """

        update_fields: list[str] = []

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )
            update_fields.append(field)

        instance.full_clean()

        instance.save(
            update_fields=update_fields,
        )

        return instance

    @staticmethod
    @transaction.atomic
    def archive(
        *,
        instance: Department,
        user: User | None = None,
    ) -> Department:
        """
        Archive (soft delete) a department.
        """

        instance.delete(
            user=user,
        )

        instance.refresh_from_db()

        return instance

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        instance: Department,
    ) -> Department:
        """
        Restore a department.
        """

        instance.restore()

        instance.refresh_from_db()

        return instance

    @staticmethod
    @transaction.atomic
    def delete(
        *,
        instance: Department,
        user: User | None = None,
    ) -> Department:
        """
        Backward-compatible alias for archive().
        """

        return DepartmentService.archive(
            instance=instance,
            user=user,
        )


def create_department(
    *,
    validated_data: DepartmentData,
) -> Department:
    """
    Legacy alias for DepartmentService.create().
    """

    return DepartmentService.create(
        validated_data=validated_data,
    )


def update_department(
    *,
    instance: Department,
    validated_data: DepartmentData,
) -> Department:
    """
    Legacy alias for DepartmentService.update().
    """

    return DepartmentService.update(
        instance=instance,
        validated_data=validated_data,
    )


def delete_department(
    *,
    instance: Department,
    user: User | None = None,
) -> Department:
    """
    Legacy alias for DepartmentService.delete().
    """

    return DepartmentService.delete(
        instance=instance,
        user=user,
    )


__all__ = (
    "DepartmentService",
    "create_department",
    "update_department",
    "delete_department",
)
