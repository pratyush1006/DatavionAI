"""
Platform bootstrap selector.

Resolves runtime context required by DatavionOS bootstrap.

Resolution:

User
 |
 +-------------------------------+
 |                               |
TenantContext                    Employee
 |                               |
 v                               v
Tenant                      Organization
                                 |
              +------------------+
              |
              v
       Organization RBAC
              |
              v
       Platform RBAC
              |
              v
      Effective Permissions
              |
              v
 Platform Bootstrap Context
"""

from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import get_user_model

from apps.datavionos.resolvers.permissions import (
    permission_resolver,
)
from apps.organization.employees.models import (
    Employee,
)
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.rbac.resolvers import (
    resolve_organization_roles,
    resolve_user_roles,
)
from apps.platform.tenancy.context import (
    get_tenant_context,
)
from apps.platform.tenancy.models import (
    Tenant,
    TenantMembership,
)

User = get_user_model()


@dataclass(
    frozen=True,
    slots=True,
)
class PlatformBootstrapContext:
    """
    Immutable DatavionOS runtime context.
    """

    user: User

    tenant: Tenant | None

    tenant_membership: TenantMembership | None

    organization: Organization | None

    employee: Employee | None

    subscription: object | None

    platform_roles: tuple[str, ...]

    organization_roles: tuple[str, ...]

    permissions: frozenset[str]


class PlatformBootstrapSelector:
    """
    Resolve DatavionOS runtime bootstrap context.
    """

    def get(
        self,
        *,
        user: User,
    ) -> PlatformBootstrapContext:
        """
        Return runtime bootstrap context.
        """

        tenant_context = get_tenant_context()

        tenant = tenant_context.tenant if tenant_context else None

        tenant_membership = tenant_context.membership if tenant_context else None

        employee = self._get_employee(
            user=user,
            tenant=tenant,
        )

        organization = self._get_organization(
            user=user,
            tenant=tenant,
            employee=employee,
        )

        subscription = self._get_subscription(
            tenant=tenant,
        )

        platform_roles = self._get_platform_roles(
            user=user,
        )

        organization_roles = self._get_organization_roles(
            user=user,
            organization=organization,
        )

        permissions = frozenset(
            permission_resolver.resolve(
                user=user,
                organization=organization,
            )
        )

        return PlatformBootstrapContext(
            user=user,
            tenant=tenant,
            tenant_membership=tenant_membership,
            organization=organization,
            employee=employee,
            subscription=subscription,
            platform_roles=platform_roles,
            organization_roles=organization_roles,
            permissions=permissions,
        )

    def _get_employee(
        self,
        *,
        user: User,
        tenant: Tenant | None,
    ) -> Employee | None:
        """
        Resolve tenant scoped employee profile.
        """

        queryset = Employee.objects.select_related(
            "organization",
            "department",
            "team",
        ).filter(
            user=user,
        )

        if tenant is not None:
            queryset = queryset.filter(
                organization__tenant=tenant,
            )

        return queryset.first()

    def _get_organization(
        self,
        *,
        user: User,
        tenant: Tenant | None,
        employee: Employee | None,
    ) -> Organization | None:
        """
        Resolve organization context.

        Resolution order:

        1. Employee organization
        2. Organization RBAC assignment
        """

        if employee is not None:
            return employee.organization

        if tenant is None:
            return None

        return (
            Organization.objects.filter(
                tenant=tenant,
                organization_roles__user=user,
                organization_roles__is_active=True,
            )
            .distinct()
            .first()
        )

    def _get_subscription(
        self,
        *,
        tenant: Tenant | None,
    ) -> object | None:
        """
        Resolve tenant subscription.
        """

        if tenant is None:
            return None

        return getattr(
            tenant,
            "subscription",
            None,
        )

    def _get_platform_roles(
        self,
        *,
        user: User,
    ) -> tuple[str, ...]:
        """
        Resolve global platform roles.
        """

        return tuple(
            role.name
            for role in resolve_user_roles(
                user=user,
            )
        )

    def _get_organization_roles(
        self,
        *,
        user: User,
        organization: Organization | None,
    ) -> tuple[str, ...]:
        """
        Resolve organization roles.
        """

        if organization is None:
            return ()

        return tuple(
            role.name
            for role in resolve_organization_roles(
                user=user,
                organization=organization,
            )
        )


platform_bootstrap_selector = PlatformBootstrapSelector()


__all__ = (
    "PlatformBootstrapContext",
    "PlatformBootstrapSelector",
    "platform_bootstrap_selector",
)
