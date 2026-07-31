"""
Bootstrap DatavionOS initial SaaS environment.

Creates:

- Tenant
- Tenant settings
- Organization
- Organization profile
- Organization settings
- Admin user
- Tenant membership
- Tenant preference
- Organization role
- Global user role

Safe to run multiple times.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

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


class Command(
    BaseCommand,
):
    """
    Create DatavionOS demo environment.
    """

    help = "Bootstrap DatavionOS SaaS environment."

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ):

        self.stdout.write("Bootstrapping DatavionOS...")

        #
        # Tenant
        #
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

        #
        # Organization
        #
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

        #
        # Admin User
        #
        user, created = User.objects.get_or_create(
            email="admin@datavion.ai",
            defaults={
                "first_name": "Datavion",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if created:
            user.set_password("ChangeMe@123")

            user.save(
                update_fields=[
                    "password",
                ],
            )

        #
        # Tenant membership
        #
        TenantMembership.objects.get_or_create(
            tenant=tenant,
            user=user,
            defaults={
                "is_owner": True,
                "status": "active",
            },
        )

        UserTenantPreference.objects.get_or_create(
            user=user,
            defaults={
                "tenant": tenant,
            },
        )

        #
        # RBAC
        #
        owner_role = Role.objects.get(
            code="organization_owner",
        )

        UserRole.objects.get_or_create(
            user=user,
            role=owner_role,
        )

        OrganizationRole.objects.get_or_create(
            organization=organization,
            user=user,
            role=owner_role,
            defaults={
                "is_primary": True,
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("DatavionOS bootstrap completed."))

        self.stdout.write("Admin login:")

        self.stdout.write("Email: admin@datavion.ai")

        self.stdout.write("Password: ChangeMe@123")
