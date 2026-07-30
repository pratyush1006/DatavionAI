"""
Department member domain services.

Handles employee assignment and membership
management inside departments.
"""

from __future__ import annotations

from django.db import transaction

from apps.organization.departments.models import (
    Department,
    DepartmentMember,
    DepartmentRole,
)
from apps.organization.employees.models import (
    Employee,
)


class DepartmentMemberService:
    """
    Department membership business services.
    """

    @staticmethod
    @transaction.atomic
    def assign(
        *,
        department: Department,
        employee: Employee,
        role: DepartmentRole | None = None,
        title: str = "",
        is_primary: bool = False,
    ) -> DepartmentMember:
        """
        Assign employee to department.
        """

        if is_primary:
            DepartmentMember.objects.filter(
                employee=employee,
                is_primary=True,
            ).update(
                is_primary=False,
            )

        member = DepartmentMember(
            department=department,
            employee=employee,
            role=role,
            title=title,
            is_primary=is_primary,
        )

        member.full_clean()

        member.save()

        return member

    @staticmethod
    @transaction.atomic
    def change_role(
        *,
        instance: DepartmentMember,
        role: DepartmentRole | None,
    ) -> DepartmentMember:
        """
        Change department role.
        """

        instance.role = role

        instance.full_clean()

        instance.save(
            update_fields=[
                "role",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def set_primary(
        *,
        instance: DepartmentMember,
    ) -> DepartmentMember:
        """
        Mark membership as primary.
        """

        DepartmentMember.objects.filter(
            employee=instance.employee,
            is_primary=True,
        ).exclude(
            id=instance.id,
        ).update(
            is_primary=False,
        )

        instance.is_primary = True

        instance.save(
            update_fields=[
                "is_primary",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def deactivate(
        *,
        instance: DepartmentMember,
    ) -> DepartmentMember:
        """
        Deactivate membership.
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
    def remove(
        *,
        instance: DepartmentMember,
    ) -> None:
        """
        Remove employee from department.
        """

        instance.delete()


__all__ = ("DepartmentMemberService",)
