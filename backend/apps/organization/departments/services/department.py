"""
Department domain services.

Business rules for department lifecycle
and management operations.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.organization.departments.constants import (
    DepartmentStatus,
)
from apps.organization.departments.models import (
    Department,
)
from apps.platform.accounts.models import User

type DepartmentData = Mapping[str, Any]


class DepartmentService:
    """
    Domain services for Department management.
    """

    # ==========================================================
    # Creation
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: DepartmentData,
    ) -> Department:
        """
        Create department.
        """

        department = Department(
            **validated_data,
        )

        department.full_clean()

        department.save()

        return department

    # ==========================================================
    # Update
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Department,
        validated_data: DepartmentData,
    ) -> Department:
        """
        Update department fields.
        """

        update_fields: list[str] = []

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

            update_fields.append(
                field,
            )

        instance.full_clean()

        instance.save(
            update_fields=update_fields,
        )

        return instance

    # ==========================================================
    # Activation
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: Department,
    ) -> Department:
        """
        Activate department.

        INACTIVE/CLOSED
                |
                v
              ACTIVE
        """

        instance.status = DepartmentStatus.ACTIVE

        instance.is_active = True

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "is_active",
            ],
        )

        return instance

    # ==========================================================
    # Deactivation
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        instance: Department,
    ) -> Department:
        """
        Deactivate department.
        """

        instance.status = DepartmentStatus.INACTIVE

        instance.is_active = False

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "is_active",
            ],
        )

        return instance

    # ==========================================================
    # Maintenance
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def put_under_maintenance(
        *,
        instance: Department,
    ) -> Department:
        """
        Put department under maintenance.
        """

        instance.status = DepartmentStatus.UNDER_MAINTENANCE

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
            ],
        )

        return instance

    # ==========================================================
    # Closure
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def close(
        *,
        instance: Department,
    ) -> Department:
        """
        Permanently close department operationally.
        """

        instance.status = DepartmentStatus.CLOSED

        instance.is_active = False

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "is_active",
            ],
        )

        return instance

    # ==========================================================
    # Archive / Delete
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def archive(
        *,
        instance: Department,
        user: User | None = None,
    ) -> Department:
        """
        Soft delete department.
        """

        instance.delete(
            user=user,
        )

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
        Delete alias.
        """

        return DepartmentService.archive(
            instance=instance,
            user=user,
        )

    # ==========================================================
    # Restore
    # ==========================================================

    @staticmethod
    @transaction.atomic
    def restore(
        *,
        instance: Department,
    ) -> Department:
        """
        Restore deleted department.
        """

        instance.restore()

        instance.status = DepartmentStatus.ACTIVE

        instance.is_active = True

        instance.save(
            update_fields=[
                "status",
                "is_active",
            ],
        )

        instance.refresh_from_db()

        return instance


# ==============================================================
# Compatibility functions
# ==============================================================


def create_department(
    *,
    validated_data: DepartmentData,
) -> Department:

    return DepartmentService.create(
        validated_data=validated_data,
    )


def update_department(
    *,
    instance: Department,
    validated_data: DepartmentData,
) -> Department:

    return DepartmentService.update(
        instance=instance,
        validated_data=validated_data,
    )


def delete_department(
    *,
    instance: Department,
    user: User | None = None,
) -> Department:

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
