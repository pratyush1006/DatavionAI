"""
Provider API tests.

Tests:
- Create provider
- List providers
- Retrieve provider
- Update provider
"""

from __future__ import annotations

from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.clinical.providers.models import Provider
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization
from apps.platform.rbac.models import (
    Permission,
    Role,
    RolePermission,
    UserRole,
)
from apps.platform.tenancy.context import (
    TenantContext,
    clear_current_tenant,
    set_tenant_context,
)
from apps.platform.tenancy.models import (
    Tenant,
    TenantMembership,
)

User = get_user_model()


class ProviderAPITestCase(APITestCase):
    """
    Provider CRUD API test suite.
    """

    LIST_URL = "providers:provider-list-create"

    DETAIL_URL = "providers:provider-detail"

    def setUp(self):
        """
        Prepare SaaS tenant,
        organization,
        user,
        employee and RBAC.
        """

        # =====================================================
        # Tenant
        # =====================================================

        self.tenant = Tenant.objects.create(
            name="Test Tenant",
            slug="test-tenant",
        )

        # =====================================================
        # Organization
        # =====================================================

        self.organization = Organization.objects.create(
            tenant=self.tenant,
            name="Test Clinic",
            slug="test-clinic",
        )

        # =====================================================
        # User
        # =====================================================

        self.user = User.objects.create_user(
            email="admin@test.com",
            password="password123",
            organization=self.organization,
            is_verified=True,
        )

        self.client.force_authenticate(
            user=self.user,
        )

        self.client.credentials(
            HTTP_X_TENANT_ID=str(
                self.tenant.id,
            ),
        )

        # =====================================================
        # Tenant Membership
        # =====================================================

        self.membership = TenantMembership.objects.create(
            tenant=self.tenant,
            user=self.user,
            is_owner=True,
        )

        # =====================================================
        # Employee
        # =====================================================

        self.employee = Employee.objects.create(
            organization=self.organization,
            user=self.user,
            employee_code="EMP001",
            designation="Doctor",
            work_email="doctor@test.com",
            phone_number="+919999999999",
            joining_date=date.today(),
        )

        # =====================================================
        # RBAC
        # =====================================================

        self.create_rbac()

    def tearDown(self):
        """
        Clear tenant context.
        """

        clear_current_tenant()

        super().tearDown()

    # =========================================================
    # Tenant Context
    # =========================================================

    def activate_tenant_context(self):
        """
        Activate DatavionOS tenant context.

        APITestCase does not execute
        TenantMiddleware lifecycle.
        """

        set_tenant_context(
            TenantContext(
                tenant=self.tenant,
                user=self.user,
                membership=self.membership,
            )
        )

    # =========================================================
    # RBAC
    # =========================================================

    def create_rbac(self):
        """
        Create provider permissions.
        """

        role, _ = Role.objects.get_or_create(
            code="clinic_admin",
            defaults={
                "name": "Clinic Admin",
                "is_system": True,
            },
        )

        permissions = {
            "providers.view": "view",
            "providers.create": "create",
            "providers.update": "update",
            "providers.verify": "verify",
            "providers.activate": "activate",
            "providers.deactivate": "deactivate",
            "providers.assign": "assign",
        }

        for code, action in permissions.items():
            permission, _ = Permission.objects.get_or_create(
                code=code,
                defaults={
                    "name": code.replace(
                        ".",
                        " ",
                    ).title(),
                    "module": "providers",
                    "action": action,
                },
            )

            RolePermission.objects.get_or_create(
                role=role,
                permission=permission,
            )

        UserRole.objects.get_or_create(
            user=self.user,
            role=role,
        )

    # =========================================================
    # Helpers
    # =========================================================

    def provider_payload(self):
        """
        Valid provider creation payload.
        """

        return {
            "employee": str(
                self.employee.id,
            ),
            "provider_number": "DOC-001",
            "provider_type": "physician",
            "specialization": "Cardiology",
        }

    def create_provider(self):
        """
        Create provider through workflow API.
        """

        self.activate_tenant_context()

        try:
            response = self.client.post(
                reverse(
                    self.LIST_URL,
                ),
                self.provider_payload(),
                format="json",
            )

        finally:
            clear_current_tenant()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.data,
        )

        return Provider.objects.get(
            id=response.data["id"],
        )

    # =========================================================
    # Tests
    # =========================================================

    def test_create_provider(self):
        """
        Test provider creation.
        """

        provider = self.create_provider()

        self.assertIsNotNone(
            provider.id,
        )

    def test_list_provider(self):
        """
        Test provider listing.
        """

        self.create_provider()

        self.activate_tenant_context()

        try:
            response = self.client.get(
                reverse(
                    self.LIST_URL,
                ),
            )

        finally:
            clear_current_tenant()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_retrieve_provider(self):
        """
        Test provider retrieval.
        """

        provider = self.create_provider()

        self.activate_tenant_context()

        try:
            response = self.client.get(
                reverse(
                    self.DETAIL_URL,
                    kwargs={
                        "provider_id": provider.id,
                    },
                ),
            )

        finally:
            clear_current_tenant()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_provider(self):
        """
        Test provider update.
        """

        provider = self.create_provider()

        self.activate_tenant_context()

        try:
            response = self.client.patch(
                reverse(
                    self.DETAIL_URL,
                    kwargs={
                        "provider_id": provider.id,
                    },
                ),
                {
                    "specialization": "Neurology",
                },
                format="json",
            )

        finally:
            clear_current_tenant()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
