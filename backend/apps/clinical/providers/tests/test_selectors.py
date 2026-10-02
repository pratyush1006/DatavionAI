"""
Provider selector tests.

Validates provider read/query layer.

Coverage:

- queryset
- list
- get
- organization filtering
- active providers
- accepting patients
- provider type filtering
- search
- exists
- count
"""

from __future__ import annotations

from datetime import date
from uuid import uuid4

from django.test import TestCase

from apps.clinical.providers.constants import (
    ProviderStatus,
)
from apps.clinical.providers.models import (
    Provider,
)
from apps.clinical.providers.selectors.provider import (
    ProviderSelector,
)
from apps.organization.employees.models import Employee
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.tenancy.models import Tenant


class ProviderSelectorTestCase(
    TestCase,
):
    """
    Provider selector test suite.
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

        self.other_organization = Organization.objects.create(
            tenant=self.tenant,
            name="Other Healthcare",
            display_name="Other Healthcare",
            code=(f"OTH-{uuid4().hex[:6].upper()}"),
            slug=(f"other-{uuid4().hex[:8]}"),
            organization_type="CLINIC",
            status="ACTIVE",
            email="other@datavion.test",
        )

        self.user = User.objects.create_user(
            email=(f"selector.{uuid4().hex[:8]}@datavion.ai"),
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
            provider_number="DOC-SELECTOR-001",
            provider_type="physician",
            years_of_experience=5,
            bio="Selector Provider",
            status=ProviderStatus.ACTIVE,
            is_accepting_patients=True,
        )

        self.other_employee = Employee.objects.create(
            organization=self.other_organization,
            user=User.objects.create_user(
                email=(f"other.selector.{uuid4().hex[:8]}@datavion.ai"),
                password="TestPassword@123",
            ),
            employee_code=(f"EMP-{uuid4().hex[:8].upper()}"),
            designation="Specialist",
            work_email=(f"other.selector.{uuid4().hex[:8]}@datavion.ai"),
            phone_number="8888888888",
            employment_type="full_time",
            status="active",
            joining_date=date.today(),
        )

        self.other_provider = Provider.objects.create(
            organization=self.other_organization,
            employee=self.other_employee,
            provider_number="DOC-OTHER-001",
            provider_type="specialist",
            years_of_experience=10,
            bio="Other Organization Provider",
            status=ProviderStatus.ACTIVE,
            is_accepting_patients=True,
        )

    def test_queryset_returns_providers(self):

        queryset = ProviderSelector.queryset()

        self.assertIn(
            self.provider,
            queryset,
        )

    def test_list_returns_all_providers(self):

        providers = ProviderSelector.list()

        self.assertEqual(
            providers.count(),
            2,
        )

    def test_get_provider(self):

        provider = ProviderSelector.get(
            provider_id=self.provider.id,
        )

        self.assertEqual(
            provider.id,
            self.provider.id,
        )

    def test_list_by_organization(self):

        providers = ProviderSelector.list_by_organization(
            organization=self.organization,
        )

        self.assertIn(
            self.provider,
            providers,
        )

        self.assertNotIn(
            self.other_provider,
            providers,
        )

    def test_list_active(self):

        providers = ProviderSelector.list_active(
            organization=self.organization,
        )

        self.assertIn(
            self.provider,
            providers,
        )

    def test_list_accepting_patients(self):

        providers = ProviderSelector.list_accepting_patients(
            organization=self.organization,
        )

        self.assertIn(
            self.provider,
            providers,
        )

    def test_list_by_provider_type(self):

        providers = ProviderSelector.list_by_provider_type(
            organization=self.organization,
            provider_type="physician",
        )

        self.assertIn(
            self.provider,
            providers,
        )

    def test_search_provider_number(self):

        providers = ProviderSelector.search(
            organization=self.organization,
            query="DOC-SELECTOR",
        )

        self.assertIn(
            self.provider,
            providers,
        )

    def test_exists(self):

        exists = ProviderSelector.exists(
            provider_id=self.provider.id,
        )

        self.assertTrue(
            exists,
        )

    def test_count_by_organization(self):

        count = ProviderSelector.count(
            organization=self.organization,
        )

        self.assertEqual(
            count,
            1,
        )
