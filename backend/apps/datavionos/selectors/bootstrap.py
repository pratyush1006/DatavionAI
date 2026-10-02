"""
Platform bootstrap selector.

Resolves the authenticated user's runtime context required by
DatavionOS bootstrap.

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

Responsibilities
----------------
This selector resolves:

- Tenant context
- Tenant membership
- Employee context
- Organization context
- Platform roles
- Organization roles
- Effective permissions

It does NOT resolve:

- SaaS subscriptions
- SaaS entitlements
- Module availability
- Navigation
- Dashboard
- Feature flags

Those responsibilities belong to the corresponding
DatavionOS services, selectors, and builders.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import get_user_model

from apps.datavionos.resolvers.permissions import (
    permission_resolver,
)
from apps.organization.departments.models import DepartmentMember
from apps.organization.employees.models import (
    Employee,
)
from apps.organization.employees.models.employee_assignment import EmployeeAssignment
from apps.organization.teams.models import TeamMember
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

    access_scope: dict[str, tuple[str, ...]]


class PlatformBootstrapSelector:
    """
    Resolve DatavionOS runtime bootstrap context.

    The selector is intentionally limited to identity, tenant,
    organization, RBAC, and effective permission resolution.

    SaaS entitlement resolution is deliberately excluded from this
    selector and remains owned by EntitlementResolver.
    """

    def get(
        self,
        *,
        user: User,
    ) -> PlatformBootstrapContext:
        """
        Return the runtime bootstrap context for the authenticated user.
        """

        tenant_context = get_tenant_context()

        tenant = tenant_context.tenant if tenant_context else None

        tenant_membership = tenant_context.membership if tenant_context else None

        # A first-time self-service signup has no browser tenant header or
        # saved preference yet. Resolve the owner's active membership so the
        # first dashboard bootstrap is scoped to the organization just
        # provisioned, rather than returning an empty workspace.
        if tenant is None:
            tenant_membership = (
                TenantMembership.objects.filter(
                    user=user,
                    status=TenantMembership.Status.ACTIVE,
                )
                .select_related("tenant")
                .order_by("-is_owner", "created_at")
                .first()
            )
            tenant = tenant_membership.tenant if tenant_membership is not None else None

        # Platform operators are global users and may not have a tenant
        # membership. Their selected organization is still a valid workspace
        # choice, so use its tenant before resolving runtime context.
        if tenant is None:
            selected_organization = getattr(user, "organization", None)
            if selected_organization is not None and selected_organization.is_active:
                tenant = selected_organization.tenant

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
            organization=organization,
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
        access_scope = self._get_access_scope(user=user, employee=employee)

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
            access_scope=access_scope,
        )

    @staticmethod
    def _get_access_scope(
        *, user: User, employee: Employee | None
    ) -> dict[str, tuple[str, ...]]:
        """Resolve direct department and team scope for downstream consumers.

        Roles grant capabilities; these memberships constrain the operational
        context in which those capabilities are presented and enforced.
        """
        department_ids: set[str] = set()
        team_ids: set[str] = set()
        if employee is not None:
            department_ids.update(
                str(value)
                for value in DepartmentMember.objects.filter(
                    employee=employee, is_active=True
                ).values_list("department_id", flat=True)
            )
            assignments = EmployeeAssignment.objects.filter(
                employee=employee, is_current=True
            )
            department_ids.update(
                str(value)
                for value in assignments.values_list("department_id", flat=True)
            )
            team_ids.update(
                str(value)
                for value in assignments.exclude(team_id__isnull=True).values_list(
                    "team_id", flat=True
                )
            )
        team_ids.update(
            str(value)
            for value in TeamMember.objects.filter(
                user=user, status="ACTIVE"
            ).values_list("team_id", flat=True)
        )
        return {
            "department_ids": tuple(sorted(department_ids)),
            "team_ids": tuple(sorted(team_ids)),
        }

    # ==================================================================
    # Employee
    # ==================================================================

    @staticmethod
    def _get_employee(
        *,
        user: User,
        tenant: Tenant | None,
    ) -> Employee | None:
        """
        Resolve the tenant-scoped employee profile.

        Employee is the organization employee aggregate root.

        The Employee model owns direct relationships to:

        - organization
        - user
        - manager
        - profile
        - provider

        Department and team assignments are separate bounded contexts
        and are intentionally not joined here.

        Bootstrap currently requires only the employee's organization
        and employee code, so only ``organization`` is eagerly loaded.
        """

        queryset = Employee.objects.select_related(
            "organization",
        ).filter(
            user=user,
        )

        if tenant is not None:
            queryset = queryset.filter(
                organization__tenant=tenant,
            )

        return queryset.first()

    # ==================================================================
    # Organization
    # ==================================================================

    @staticmethod
    def _get_organization(
        *,
        user: User,
        tenant: Tenant | None,
        employee: Employee | None,
    ) -> Organization | None:
        """
        Resolve the organization context.

        Resolution order:

        1. Employee organization
        2. User's selected/default organization (platform operators)
        3. Active organization RBAC assignment

        Employee organization is authoritative when an employee
        exists for the current tenant.
        """

        if employee is not None:
            return employee.organization

        if tenant is None:
            return None

        # Platform administrators have a global UserRole and often do not
        # have a tenant-specific OrganizationRole.  Preserve the selected
        # organization context when it belongs to the resolved tenant so the
        # platform control plane can load its entitled module runtime.
        selected_organization = getattr(user, "organization", None)
        if (
            selected_organization is not None
            and selected_organization.tenant_id == tenant.id
        ):
            return selected_organization

        return (
            Organization.objects.filter(
                tenant=tenant,
                organization_roles__user=user,
                organization_roles__is_active=True,
            )
            .distinct()
            .first()
        )

    # ==================================================================
    # Subscription
    # ==================================================================

    @staticmethod
    def _get_subscription(
        *,
        organization: Organization | None,
    ) -> object | None:
        """
        Resolve the tenant subscription reference.

        This is retained as runtime context compatibility only.

        SaaS entitlement decisions are not performed here.
        EntitlementResolver owns entitlement resolution.
        """

        if organization is None:
            return None

        return getattr(
            organization,
            "saas_subscription",
            None,
        )

    # ==================================================================
    # Platform RBAC
    # ==================================================================

    @staticmethod
    def _get_platform_roles(
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

    # ==================================================================
    # Organization RBAC
    # ==================================================================

    @staticmethod
    def _get_organization_roles(
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
