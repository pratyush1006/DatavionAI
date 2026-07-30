"""
Department role domain services.

Manages department-scoped roles and permissions.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.organization.departments.models import (
    Department,
    DepartmentRole,
)
from django.db import transaction

type DepartmentRoleData = Mapping[str, Any]


class DepartmentRoleService:
    """
    Business services for department roles.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        department: Department,
        validated_data: DepartmentRoleData,
    ) -> DepartmentRole:
        """
        Create department role.
        """

        role = DepartmentRole(
            department=department,
            **validated_data,
        )

        role.full_clean()

        role.save()

        return role

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: DepartmentRole,
        validated_data: DepartmentRoleData,
    ) -> DepartmentRole:
        """
        Update department role.
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

    @staticmethod
    @transaction.atomic
    def activate(
        *,
        instance: DepartmentRole,
    ) -> DepartmentRole:
        """
        Activate role.
        """

        instance.is_active = True

        instance.save(
            update_fields=[
                "is_active",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        instance: DepartmentRole,
    ) -> DepartmentRole:
        """
        Deactivate role.
        """

        instance.is_active = False

        instance.save(
            update_fields=[
                "is_active",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def update_permissions(
        *,
        instance: DepartmentRole,
        permissions: list[str],
    ) -> DepartmentRole:
        """
        Update role permissions.
        """

        instance.permissions = permissions

        instance.save(
            update_fields=[
                "permissions",
            ],
        )

        return instance


__all__ = ("DepartmentRoleService",)
