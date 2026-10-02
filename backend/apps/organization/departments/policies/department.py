"""
Department authorization policies.

Uses DatavionOS RBAC engine.

Authorization flow:

Workflow
    |
    v
DepartmentPolicy
    |
    v
RBAC Engine
    |
    v
OrganizationRole + RolePermission
"""

from __future__ import annotations

from apps.organization.departments.models import Department
from apps.platform.accounts.models import User
from apps.platform.rbac.engines import (
    user_has_permission,
)


class DepartmentPolicy:
    """
    Department authorization policy.

    Domain workflows must use the
    platform RBAC engine.
    """

    def can_create(
        self,
        *,
        actor: User,
        organization,
    ) -> bool:
        """
        Check department creation permission.
        """

        return user_has_permission(
            user=actor,
            permission="departments.create",
            organization=organization,
        )

    def can_manage(
        self,
        *,
        actor: User,
        department: Department,
    ) -> bool:
        """
        Check department update permission.
        """

        return user_has_permission(
            user=actor,
            permission="departments.update",
            organization=department.organization,
        )

    def can_delete(
        self,
        *,
        actor: User,
        department: Department,
    ) -> bool:
        """
        Check department delete permission.
        """

        return user_has_permission(
            user=actor,
            permission="departments.delete",
            organization=department.organization,
        )

    def can_manage_members(
        self,
        *,
        actor: User,
        department: Department,
    ) -> bool:
        """
        Check member management permission.
        """

        return user_has_permission(
            user=actor,
            permission="departments.assign",
            organization=department.organization,
        )

    def can_manage_roles(
        self,
        *,
        actor: User,
        department: Department,
    ) -> bool:
        """
        Check role management permission.
        """

        return user_has_permission(
            user=actor,
            permission="rbac.assign",
            organization=department.organization,
        )

    def can_manage_settings(
        self,
        *,
        actor: User,
        department: Department,
    ) -> bool:
        """
        Check department settings permission.
        """

        return user_has_permission(
            user=actor,
            permission="departments.update",
            organization=department.organization,
        )

    def can_manage_hierarchy(
        self,
        *,
        actor: User,
        department: Department,
    ) -> bool:
        """
        Check hierarchy permission.
        """

        return user_has_permission(
            user=actor,
            permission="departments.update",
            organization=department.organization,
        )


__all__ = ("DepartmentPolicy",)
