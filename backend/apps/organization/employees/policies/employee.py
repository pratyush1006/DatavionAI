"""
Employee authorization policies.

Uses DatavionOS RBAC engine.

Authorization flow:

Workflow
    |
    v
EmployeePolicy
    |
    v
RBAC Engine
    |
    v
OrganizationRole + RolePermission
"""

from __future__ import annotations

from apps.organization.employees.models import (
    Employee,
)
from apps.platform.accounts.models import (
    User,
)
from apps.platform.rbac.engines import (
    user_has_permission,
)


class EmployeePolicy:
    """
    Employee authorization policy.

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
        Check employee creation permission.
        """

        return user_has_permission(
            user=actor,
            permission="employees.create",
            organization=organization,
        )

    def can_manage(
        self,
        *,
        actor: User,
        employee: Employee,
    ) -> bool:
        """
        Check employee update permission.
        """

        return user_has_permission(
            user=actor,
            permission="employees.update",
            organization=employee.organization,
        )

    def can_delete(
        self,
        *,
        actor: User,
        employee: Employee,
    ) -> bool:
        """
        Check employee deletion permission.
        """

        return user_has_permission(
            user=actor,
            permission="employees.delete",
            organization=employee.organization,
        )

    def can_assign(
        self,
        *,
        actor: User,
        employee: Employee,
    ) -> bool:
        """
        Check employee assignment permission.

        Covers:

        - Department assignment
        - Team assignment
        - Supervisor assignment
        """

        return user_has_permission(
            user=actor,
            permission="employees.assign",
            organization=employee.organization,
        )

    def can_manage_assignments(
        self,
        *,
        actor: User,
        employee: Employee,
    ) -> bool:
        """
        Explicit assignment workflow permission.
        """

        return self.can_assign(
            actor=actor,
            employee=employee,
        )

    def can_activate(
        self,
        *,
        actor: User,
        employee: Employee,
    ) -> bool:
        """
        Check employee activation permission.
        """

        return user_has_permission(
            user=actor,
            permission="employees.activate",
            organization=employee.organization,
        )

    def can_deactivate(
        self,
        *,
        actor: User,
        employee: Employee,
    ) -> bool:
        """
        Check employee deactivation permission.
        """

        return user_has_permission(
            user=actor,
            permission="employees.deactivate",
            organization=employee.organization,
        )

    def can_manage_contracts(
        self,
        *,
        actor: User,
        employee: Employee,
    ) -> bool:
        """
        Check employee contract management permission.
        """

        return user_has_permission(
            user=actor,
            permission="employees.update",
            organization=employee.organization,
        )

    def can_onboard(
        self,
        *,
        actor: User,
        organization,
    ) -> bool:
        """
        Check employee onboarding permission.
        """

        return user_has_permission(
            user=actor,
            permission="employees.create",
            organization=organization,
        )

    def can_offboard(
        self,
        *,
        actor: User,
        employee: Employee,
    ) -> bool:
        """
        Check employee offboarding permission.
        """

        return user_has_permission(
            user=actor,
            permission="employees.deactivate",
            organization=employee.organization,
        )


__all__ = ("EmployeePolicy",)
