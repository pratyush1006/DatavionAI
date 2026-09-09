"""
Provider assignment service tests.

Validates provider assignment
domain service layer.

Coverage:

- Create assignment
- Update assignment
- Activate assignment
- Deactivate assignment
- Delete assignment
"""

from __future__ import annotations

from datetime import date
from uuid import uuid4

from django.test import TestCase

from apps.clinical.providers.constants import (
    ProviderAssignmentStatus,
)
from apps.clinical.providers.models import (
    Provider,
)
from apps.clinical.providers.services.assignment import (
    ProviderAssignmentService,
)
from apps.organization.departments.models import Department
from apps.organization.employees.models import Employee
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant


class ProviderAssignmentServiceTestCase(
    TestCase,
):
    """
    Provider assignment service tests.
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

        self.user = User.objects.create_user(
            email=(f"assignment.{uuid4().hex[:8]}@datavion.ai"),
            password="TestPassword@123",
        )

        self.employee = Employee.objects.create(
            organization=self.organization,
            user=self.user,
            employee_code=(f"EMP-{uuid4().hex[:8].upper()}"),
            designation="Physician",
            work_email=self.user.email,
            phone_number="9999999999",
            employment_type="full_time",
            status="active",
            joining_date=date.today(),
        )

        self.provider = Provider.objects.create(
            organization=self.organization,
            employee=self.employee,
            provider_number=(f"DOC-{uuid4().hex[:8].upper()}"),
            provider_type="physician",
            years_of_experience=5,
            bio="Assignment service provider",
        )

        self.department = Department.objects.create(
            organization=self.organization,
            name="Cardiology",
            code=(f"CARD-{uuid4().hex[:6].upper()}"),
        )

    def create_assignment(self):

        return ProviderAssignmentService.create(
            validated_data={
                "organization": self.organization,
                "provider": self.provider,
                "department": self.department,
            },
        )

    def test_create_assignment(self):

        assignment = self.create_assignment()

        self.assertIsNotNone(
            assignment.id,
        )

        self.assertEqual(
            assignment.provider,
            self.provider,
        )

        self.assertEqual(
            assignment.organization,
            self.organization,
        )

        self.assertEqual(
            assignment.department,
            self.department,
        )

    def test_update_assignment(self):

        assignment = self.create_assignment()

        updated = ProviderAssignmentService.update(
            instance=assignment,
            validated_data={
                "department": self.department,
            },
        )

        self.assertEqual(
            updated.department,
            self.department,
        )

    def test_activate_assignment(self):

        assignment = self.create_assignment()

        activated = ProviderAssignmentService.activate(
            instance=assignment,
        )

        self.assertEqual(
            activated.status,
            ProviderAssignmentStatus.ACTIVE,
        )

    def test_deactivate_assignment(self):

        assignment = self.create_assignment()

        deactivated = ProviderAssignmentService.deactivate(
            instance=assignment,
        )

        self.assertEqual(
            deactivated.status,
            ProviderAssignmentStatus.INACTIVE,
        )

    def test_delete_assignment(self):

        assignment = self.create_assignment()

        ProviderAssignmentService.delete(
            instance=assignment,
        )

        assignment.refresh_from_db()

        self.assertTrue(
            assignment.is_deleted,
        )
