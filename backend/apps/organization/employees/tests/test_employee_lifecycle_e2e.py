"""
Employee Lifecycle API E2E Test.

DatavionOS Employee Lifecycle:

Tenant Context
        |
Organization Context
        |
RBAC
        |
Employee API
        |
Workflow Engine
"""

from __future__ import annotations

import uuid
from datetime import date

from django.urls import reverse
from rest_framework.test import APITestCase

from apps.common.middleware.context import (
    set_current_organization,
    set_current_tenant,
)
from apps.organization.departments.models import Department
from apps.organization.employees.models import Employee
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.constants import (
    SystemRole,
)
from apps.platform.rbac.models import (
    OrganizationRole,
    Permission,
    Role,
    RolePermission,
)
from apps.platform.rbac.seed_data.role_permissions import (
    SYSTEM_ROLE_PERMISSIONS,
)
from apps.platform.rbac.seed_data.roles import (
    SYSTEM_ROLES,
)
from apps.platform.tenancy.models import Tenant


class EmployeeLifecycleE2ETestCase(
    APITestCase,
):
    """
    Complete employee lifecycle.
    """

    # =========================================================
    # RBAC SEED
    # =========================================================

    def seed_rbac(self):

        roles = {}

        for role_data in SYSTEM_ROLES:
            role, _ = Role.objects.get_or_create(
                code=role_data["code"],
                defaults=role_data,
            )

            roles[role.code] = role

        for (
            role_code,
            permissions,
        ) in SYSTEM_ROLE_PERMISSIONS.items():
            role = roles.get(
                role_code,
            )

            if not role:
                continue

            for permission_code in permissions:
                if permission_code == "*":
                    continue

                module, action = permission_code.split(".")

                permission, _ = Permission.objects.get_or_create(
                    code=permission_code,
                    defaults={
                        "module": module,
                        "action": action,
                        "scope": "organization",
                        "name": permission_code.replace(
                            ".",
                            " ",
                        ).title(),
                    },
                )

                RolePermission.objects.get_or_create(
                    role=role,
                    permission=permission,
                )

        return roles[SystemRole.ORGANIZATION_OWNER.value]

    # =========================================================
    # SETUP
    # =========================================================

    def setUp(self):

        self.tenant = Tenant.objects.create(
            name="Datavion Test Tenant",
            slug=(f"tenant-{uuid.uuid4().hex[:8]}"),
            tenant_type="ORGANIZATION",
            status="ACTIVE",
        )

        self.organization = Organization.objects.create(
            tenant=self.tenant,
            name="Datavion Healthcare Clinic",
            display_name="Datavion Healthcare Clinic",
            code=(f"DVT-{uuid.uuid4().hex[:6].upper()}"),
            slug=(f"clinic-{uuid.uuid4().hex[:8]}"),
            organization_type="CLINIC",
            status="ACTIVE",
            email="clinic@datavion.test",
        )

        self.user = User.objects.create_user(
            email="admin@datavion.test",
            password="Test@123456",
        )

        # RBAC

        owner_role = self.seed_rbac()

        OrganizationRole.objects.create(
            organization=self.organization,
            user=self.user,
            role=owner_role,
            is_primary=True,
        )

        self.department = Department.objects.create(
            organization=self.organization,
            name="Cardiology",
            code="CARDIOLOGY",
        )

        # ContextVar context

        set_current_tenant(
            self.tenant,
        )

        set_current_organization(
            self.organization,
        )

        self.client.force_authenticate(
            user=self.user,
        )

    # =========================================================
    # API HEADERS
    # =========================================================

    def headers(self):

        return {
            "HTTP_X_TENANT_ID": str(self.tenant.id),
            "HTTP_X_ORGANIZATION_ID": str(self.organization.id),
        }

    # =========================================================
    # TEST
    # =========================================================

    def test_employee_full_lifecycle(self):

        employee_code = f"E2E-{uuid.uuid4().hex[:8].upper()}"

        # CREATE

        response = self.client.post(
            reverse(
                "employee-list-create",
            ),
            {
                "organization": str(self.organization.id),
                "employee_code": employee_code,
                "designation": "API Test Doctor",
                "joining_date": str(date.today()),
                "work_email": f"{employee_code}@test.com",
                "phone_number": "9999999999",
                "employment_type": "FULL_TIME",
            },
            format="json",
            **self.headers(),
        )

        self.assertEqual(
            response.status_code,
            201,
            response.data,
        )

        employee_id = response.data["data"]["id"]

        employee = Employee.objects.get(
            id=employee_id,
        )

        # DETAIL

        response = self.client.get(
            reverse(
                "employee-detail",
                kwargs={
                    "employee_id": employee_id,
                },
            ),
            **self.headers(),
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        # UPDATE

        response = self.client.patch(
            reverse(
                "employee-detail",
                kwargs={
                    "employee_id": employee_id,
                },
            ),
            {
                "designation": "Senior Consultant",
            },
            format="json",
            **self.headers(),
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        # ASSIGNMENT

        response = self.client.post(
            reverse(
                "employee-assignment",
                kwargs={
                    "employee_id": employee_id,
                },
            ),
            {
                "department_id": str(self.department.id),
            },
            format="json",
            **self.headers(),
        )

        self.assertIn(
            response.status_code,
            [200, 201],
            response.data,
        )

        # CONTRACT

        response = self.client.post(
            reverse(
                "employee-contract",
                kwargs={
                    "employee_id": employee_id,
                },
            ),
            {
                "contract_data": {
                    "contract_number": f"CON-{uuid.uuid4().hex[:8]}",
                    "contract_type": "FULL_TIME",
                    "status": "ACTIVE",
                    "start_date": str(date.today()),
                    "is_current": True,
                }
            },
            format="json",
            **self.headers(),
        )

        self.assertIn(
            response.status_code,
            [200, 201],
            response.data,
        )

        # ACTIVATE

        response = self.client.post(
            reverse(
                "employee-activate",
                kwargs={
                    "employee_id": employee_id,
                },
            ),
            {},
            format="json",
            **self.headers(),
        )

        self.assertEqual(
            response.status_code,
            200,
            response.data,
        )

        # DEACTIVATE

        response = self.client.post(
            reverse(
                "employee-deactivate",
                kwargs={
                    "employee_id": employee_id,
                },
            ),
            {},
            format="json",
            **self.headers(),
        )

        self.assertEqual(
            response.status_code,
            200,
            response.data,
        )

        # DELETE

        response = self.client.delete(
            reverse(
                "employee-detail",
                kwargs={
                    "employee_id": employee_id,
                },
            ),
            **self.headers(),
        )

        self.assertIn(
            response.status_code,
            [200, 204],
            response.data,
        )

        employee.refresh_from_db()

        self.assertTrue(
            employee.is_deleted,
        )
