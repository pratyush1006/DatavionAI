"""
Platform bootstrap selector.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import get_user_model

from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization
from apps.platform_core.resolvers.permissions import (
    permission_resolver,
)

User = get_user_model()


@dataclass(
    frozen=True,
    slots=True,
)
class PlatformBootstrapContext:
    """
    Platform bootstrap context.
    """

    user: User

    organization: Organization | None

    employee: Employee | None

    roles: list[str]

    permissions: set[str]

    # Reserved for future SaaS modules.
    workspace: object | None = None

    subscription: object | None = None


class PlatformBootstrapSelector:
    """
    Retrieve platform bootstrap context.
    """

    def get(
        self,
        *,
        user: User,
    ) -> PlatformBootstrapContext:
        """
        Return the platform bootstrap context.
        """

        employee = self._get_employee(
            user=user,
        )

        organization = employee.organization if employee is not None else None

        roles = self._get_roles(
            user=user,
        )

        permissions = permission_resolver.resolve(
            user=user,
        )

        return PlatformBootstrapContext(
            user=user,
            organization=organization,
            employee=employee,
            roles=roles,
            permissions=permissions,
        )

    def _get_employee(
        self,
        *,
        user: User,
    ) -> Employee | None:
        """
        Return the employee profile.
        """

        return (
            Employee.objects.select_related(
                "organization",
                "department",
                "team",
            )
            .filter(
                user=user,
            )
            .first()
        )

    def _get_roles(
        self,
        *,
        user: User,
    ) -> list[str]:
        """
        Return the user's role names.
        """

        return list(
            user.groups.values_list(
                "name",
                flat=True,
            ),
        )


platform_bootstrap_selector = PlatformBootstrapSelector()


__all__ = [
    "PlatformBootstrapContext",
    "PlatformBootstrapSelector",
    "platform_bootstrap_selector",
]
