"""
Bootstrap DatavionOS initial SaaS environment.

Creates:

- Tenant
- Tenant settings
- Tenant domain
- Organization
- Organization profile
- Organization settings
- Demo admin/test user
- Tenant membership
- Tenant preference
- Employee
- Organization role
- Global user role

The command is safe to run multiple times.

The existing DatavionOS demo tenant and organization are reused when they
already exist.

The demo runtime user is:

    datavion.test@demo.local

This command provisions the complete tenant, organization, employee, and RBAC
context required by the DatavionOS platform bootstrap API.
"""

from __future__ import annotations

from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.organization.employees.constants import (
    EmploymentStatus,
    EmploymentType,
)
from apps.organization.employees.models import (
    Employee,
)
from apps.organization.employees.services import (
    create_employee,
)
from apps.platform.organizations.models import (
    Organization,
    OrganizationProfile,
    OrganizationSettings,
)
from apps.platform.rbac.models import (
    OrganizationRole,
    Role,
    UserRole,
)
from apps.platform.tenancy.models import (
    Tenant,
    TenantDomain,
    TenantMembership,
    TenantSettings,
    UserTenantPreference,
)

User = get_user_model()


class Command(BaseCommand):
    """
    Create the DatavionOS demo environment.
    """

    help = "Bootstrap DatavionOS SaaS environment."

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ):
        self.stdout.write(
            "Bootstrapping DatavionOS...",
        )

        # ==================================================================
        # Tenant
        # ==================================================================

        tenant, _ = Tenant.objects.get_or_create(
            slug="datavion-demo",
            defaults={
                "name": "DatavionOS Demo Tenant",
            },
        )

        TenantSettings.objects.get_or_create(
            tenant=tenant,
            defaults={
                "timezone": "Asia/Kolkata",
                "language": "en",
                "currency": "INR",
            },
        )

        TenantDomain.objects.get_or_create(
            tenant=tenant,
            domain="demo.datavion.ai",
            defaults={
                "is_primary": True,
                "is_verified": True,
            },
        )

        # ==================================================================
        # Organization
        # ==================================================================

        organization, _ = Organization.objects.get_or_create(
            tenant=tenant,
            code="DATAVION",
            defaults={
                "name": "Datavion Healthcare Clinic",
                "display_name": "Datavion Healthcare",
                "email": "admin@datavion.ai",
                "city": "Bangalore",
                "state": "Karnataka",
                "country": "India",
                "is_demo": True,
            },
        )

        OrganizationProfile.objects.get_or_create(
            organization=organization,
            defaults={
                "industry": "healthcare",
                "facility_type": "clinic",
                "description": ("DatavionOS healthcare demo organization."),
            },
        )

        OrganizationSettings.objects.get_or_create(
            organization=organization,
            defaults={
                "language": "en",
                "timezone": "Asia/Kolkata",
                "currency": "INR",
            },
        )

        # ==================================================================
        # Demo User
        # ==================================================================

        user, created = User.objects.get_or_create(
            email="datavion.test@demo.local",
            defaults={
                "first_name": "Datavion",
                "last_name": "Test",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if created:
            user.set_password(
                "ChangeMe@123",
            )

            user.save(
                update_fields=[
                    "password",
                ],
            )
        else:
            update_fields: list[str] = []

            if not user.is_active:
                user.is_active = True
                update_fields.append(
                    "is_active",
                )

            if not user.is_staff:
                user.is_staff = True
                update_fields.append(
                    "is_staff",
                )

            if not user.is_superuser:
                user.is_superuser = True
                update_fields.append(
                    "is_superuser",
                )

            if update_fields:
                user.save(
                    update_fields=update_fields,
                )

        # ==================================================================
        # Tenant Membership
        # ==================================================================

        membership, _ = TenantMembership.objects.get_or_create(
            tenant=tenant,
            user=user,
            defaults={
                "is_owner": True,
                "status": TenantMembership.Status.ACTIVE,
            },
        )

        membership_updates: list[str] = []

        if membership.status != TenantMembership.Status.ACTIVE:
            membership.status = TenantMembership.Status.ACTIVE
            membership_updates.append(
                "status",
            )

        if not membership.is_owner:
            membership.is_owner = True
            membership_updates.append(
                "is_owner",
            )

        if membership_updates:
            membership.save(
                update_fields=membership_updates,
            )

        # ==================================================================
        # Tenant Preference
        # ==================================================================

        UserTenantPreference.objects.update_or_create(
            user=user,
            defaults={
                "tenant": tenant,
            },
        )

        # ==================================================================
        # Employee
        # ==================================================================

        employee = Employee.objects.filter(
            organization=organization,
            user=user,
        ).first()

        if employee is None:
            employee = create_employee(
                validated_data={
                    "organization": organization,
                    "user": user,
                    "employee_code": "DATAVION-ADMIN",
                    "designation": "Organization Administrator",
                    "joining_date": date.today(),
                    "employment_type": (EmploymentType.FULL_TIME),
                    "status": (EmploymentStatus.ACTIVE),
                },
            )

        # ==================================================================
        # RBAC
        # ==================================================================

        owner_role = Role.objects.get(
            code="organization_owner",
            is_active=True,
        )

        UserRole.objects.get_or_create(
            user=user,
            role=owner_role,
        )

        organization_role, _ = OrganizationRole.objects.get_or_create(
            organization=organization,
            user=user,
            role=owner_role,
            defaults={
                "is_primary": True,
                "is_active": True,
            },
        )

        organization_role_updates: list[str] = []

        if not organization_role.is_primary:
            organization_role.is_primary = True
            organization_role_updates.append(
                "is_primary",
            )

        if not organization_role.is_active:
            organization_role.is_active = True
            organization_role_updates.append(
                "is_active",
            )

        if organization_role_updates:
            organization_role.save(
                update_fields=organization_role_updates,
            )

        # ==================================================================
        # Output
        # ==================================================================

        self.stdout.write(
            self.style.SUCCESS(
                "DatavionOS bootstrap completed.",
            ),
        )

        self.stdout.write("")
        self.stdout.write(
            "Demo environment:",
        )

        self.stdout.write(
            f"Tenant: {tenant.name}",
        )

        self.stdout.write(
            f"Organization: {organization.name}",
        )

        self.stdout.write(
            f"Employee: {employee.employee_code}",
        )

        self.stdout.write(
            "Role: organization_owner",
        )

        self.stdout.write("")
        self.stdout.write(
            "Demo login:",
        )

        self.stdout.write(
            "Email: datavion.test@demo.local",
        )

        self.stdout.write(
            "Password: ChangeMe@123",
        )
