"""
Department API end-to-end tests.

Validates:

Tenant
Organization
RBAC
Department API
Workflow execution
Soft delete
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.test import APITestCase

from apps.organization.departments.models import (
    Department,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines import (
    user_has_permission,
)
from apps.platform.rbac.models import (
    OrganizationRole,
    Permission,
    Role,
    RolePermission,
)
from apps.platform.tenancy.models import Tenant


class DepartmentAPIE2ETestCase(
    APITestCase,
):
    def setUp(
        self,
    ):

        self.user = User.objects.create_user(
            email="department.api@datavion.ai",
            password="Test@12345",
        )

        self.tenant = Tenant.objects.create(
            name="Department API Tenant",
            slug="department-api",
        )

        self.organization = Organization.objects.create(
            tenant=self.tenant,
            name="Department API Hospital",
            code="DEPT-API",
        )

        self.role = Role.objects.create(
            name="Organization Administrator",
            code="organization_admin_e2e",
        )

        OrganizationRole.objects.create(
            organization=self.organization,
            user=self.user,
            role=self.role,
        )

        for code, action in (
            (
                "departments.create",
                "create",
            ),
            (
                "departments.update",
                "update",
            ),
            (
                "departments.delete",
                "delete",
            ),
            (
                "departments.view",
                "view",
            ),
        ):
            permission = Permission.objects.create(
                code=code,
                name=code,
                module="departments",
                action=action,
                scope="organization",
            )

            RolePermission.objects.create(
                role=self.role,
                permission=permission,
            )

        self.assertTrue(
            user_has_permission(
                user=self.user,
                permission="departments.create",
                organization=self.organization,
            )
        )

        self.client.force_authenticate(
            user=self.user,
        )

        self.client.defaults.update(
            {
                "HTTP_X_TENANT_ID": str(
                    self.tenant.id,
                ),
                "HTTP_X_ORGANIZATION_ID": str(
                    self.organization.id,
                ),
            }
        )

        self.url = "/api/departments/"

    def test_department_complete_api_lifecycle(
        self,
    ):

        response = self.client.post(
            self.url,
            {
                "organization": str(
                    self.organization.id,
                ),
                "name": "Cardiology API",
                "code": "CARD-API",
                "description": "API test",
                "department_type": "CLINICAL",
                "phone": "9999999999",
                "email": ("cardiology.api@datavion.ai"),
                "location": "Block A",
            },
            format="json",
        )

        print(response.data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        department_id = response.data["data"]["id"]

        detail_url = f"{self.url}{department_id}/"

        response = self.client.get(
            self.url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.get(
            detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.patch(
            detail_url,
            {"name": ("Cardiology Advanced API")},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.delete(
            detail_url,
        )

        self.assertIn(
            response.status_code,
            (
                status.HTTP_200_OK,
                status.HTTP_204_NO_CONTENT,
            ),
        )

        department = Department.all_objects.get(
            id=department_id,
        )

        self.assertTrue(
            department.is_deleted,
        )
