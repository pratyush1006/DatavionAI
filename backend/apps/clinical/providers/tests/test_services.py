"""
Provider service tests.

Validates provider domain service layer.

Coverage:

- Create provider
- Update provider
- Verify provider
- Activate provider
- Deactivate provider
- Suspend provider
- Delete provider
- Restore provider
"""

from __future__ import annotations

from datetime import date
from uuid import uuid4

from django.test import TestCase

from apps.clinical.providers.constants import (
    ProviderStatus,
)
from apps.clinical.providers.services import (
    ProviderService,
)
from apps.organization.employees.models import Employee
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant


class ProviderServiceTestCase(
    TestCase,
):
    """
    Provider service test suite.
    """

    def setUp(self):

        self.tenant = Tenant.objects.create(
            name="Datavion Test Tenant",
            slug=(f"tenant-{uuid4().hex[:8]}"),
            tenant_type="ORGANIZATION",
            status="ACTIVE",
        )

        self.organization = Organization.objects.create(
            tenant=self.tenant,
            name="Datavion Healthcare",
            display_name="Datavion Healthcare",
            code=(f"DVT-{uuid4().hex[:6].upper()}"),
            slug=(f"clinic-{uuid4().hex[:8]}"),
            organization_type="CLINIC",
            status="ACTIVE",
            email="clinic@datavion.test",
        )

        self.employee_user = User.objects.create_user(
            email=(f"provider.service.{uuid4().hex[:8]}@datavion.ai"),
            password="TestPassword@123",
        )

        self.employee = Employee.objects.create(
            organization=self.organization,
            user=self.employee_user,
            employee_code=(f"EMP-{uuid4().hex[:8].upper()}"),
            designation="Physician",
            work_email=self.employee_user.email,
            phone_number="9999999999",
            employment_type="full_time",
            status="active",
            joining_date=date.today(),
        )

    def create_provider(self):

        return ProviderService.create(
            validated_data={
                "organization": self.organization,
                "employee": self.employee,
                "provider_number": (f"DOC-{uuid4().hex[:8].upper()}"),
                "provider_type": "physician",
                "years_of_experience": 5,
                "bio": "Service test provider",
            },
        )

    def test_create_provider(self):

        provider = self.create_provider()

        self.assertIsNotNone(
            provider.id,
        )

        self.assertEqual(
            provider.organization,
            self.organization,
        )

        self.assertEqual(
            provider.employee,
            self.employee,
        )

        self.assertEqual(
            provider.status,
            ProviderStatus.PENDING,
        )

    def test_update_provider(self):

        provider = self.create_provider()

        updated = ProviderService.update(
            instance=provider,
            validated_data={
                "bio": "Updated provider",
                "years_of_experience": 10,
            },
        )

        self.assertEqual(
            updated.bio,
            "Updated provider",
        )

        self.assertEqual(
            updated.years_of_experience,
            10,
        )

    def test_verify_provider(self):

        provider = self.create_provider()

        verified = ProviderService.verify(
            instance=provider,
        )

        self.assertEqual(
            verified.status,
            ProviderStatus.VERIFIED,
        )

    def test_activate_provider(self):

        provider = self.create_provider()

        provider.status = ProviderStatus.VERIFIED

        provider.save(
            update_fields=[
                "status",
            ],
        )

        activated = ProviderService.activate(
            instance=provider,
        )

        self.assertEqual(
            activated.status,
            ProviderStatus.ACTIVE,
        )

        self.assertTrue(
            activated.is_accepting_patients,
        )

    def test_deactivate_provider(self):

        provider = self.create_provider()

        provider.status = ProviderStatus.ACTIVE

        provider.save(
            update_fields=[
                "status",
            ],
        )

        deactivated = ProviderService.deactivate(
            instance=provider,
        )

        self.assertEqual(
            deactivated.status,
            ProviderStatus.INACTIVE,
        )

        self.assertFalse(
            deactivated.is_accepting_patients,
        )

    def test_suspend_provider(self):

        provider = self.create_provider()

        suspended = ProviderService.suspend(
            instance=provider,
        )

        self.assertEqual(
            suspended.status,
            ProviderStatus.SUSPENDED,
        )

        self.assertFalse(
            suspended.is_accepting_patients,
        )

    def test_delete_provider(self):

        provider = self.create_provider()

        ProviderService.delete(
            instance=provider,
        )

        provider.refresh_from_db()

        self.assertTrue(
            provider.is_deleted,
        )

    def test_restore_provider(self):

        provider = self.create_provider()

        ProviderService.delete(
            instance=provider,
        )

        provider.refresh_from_db()

        restored = ProviderService.restore(
            instance=provider,
        )

        self.assertFalse(
            restored.is_deleted,
        )
