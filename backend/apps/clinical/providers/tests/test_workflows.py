"""
Provider workflow tests.

Validates provider lifecycle workflows.

Coverage:

- Creation
- Verification
- Activation
- Assignment
- Update
- Deactivation
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
from apps.clinical.providers.workflows import (
    ProviderActivationRequest,
    ProviderActivationWorkflow,
    ProviderAssignmentRequest,
    ProviderAssignmentWorkflow,
    ProviderCreationRequest,
    ProviderCreationWorkflow,
    ProviderDeactivationRequest,
    ProviderDeactivationWorkflow,
    ProviderUpdateRequest,
    ProviderUpdateWorkflow,
    ProviderVerificationRequest,
    ProviderVerificationWorkflow,
)
from apps.core.workflows import (
    WorkflowContext,
)
from apps.organization.departments.models import (
    Department,
)
from apps.organization.employees.models import (
    Employee,
)
from apps.platform.accounts.models import (
    User,
)
from apps.platform.organizations.models import (
    Organization,
)
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
from apps.platform.tenancy.models import (
    Tenant,
)


class ProviderWorkflowTestCase(
    TestCase,
):
    """
    Provider workflow test suite.
    """

    # =========================================================
    # RBAC
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

                module, action = permission_code.split(".", 1)

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
            name="Provider Test Tenant",
            slug=f"tenant-{uuid4().hex[:8]}",
            tenant_type="ORGANIZATION",
            status="ACTIVE",
        )

        self.organization = Organization.objects.create(
            tenant=self.tenant,
            name="Provider Test Clinic",
            display_name="Provider Test Clinic",
            code=f"CL-{uuid4().hex[:6].upper()}",
            slug=f"clinic-{uuid4().hex[:8]}",
            organization_type="CLINIC",
            status="ACTIVE",
            email="clinic@test.com",
        )

        self.user = User.objects.create_user(
            email="provider.admin@test.com",
            password="Test@123456",
        )

        owner_role = self.seed_rbac()

        OrganizationRole.objects.create(
            organization=self.organization,
            user=self.user,
            role=owner_role,
            is_primary=True,
        )

        self.context = WorkflowContext(
            actor_id=self.user.id,
            tenant_id=self.tenant.id,
        )

        employee_user = User.objects.create_user(
            email=f"employee.{uuid4().hex[:8]}@test.com",
            password="Test@123456",
        )

        self.employee = Employee.objects.create(
            organization=self.organization,
            user=employee_user,
            employee_code=f"EMP-{uuid4().hex[:8].upper()}",
            designation="Physician",
            work_email=employee_user.email,
            phone_number="9999999999",
            employment_type="full_time",
            status="active",
            joining_date=date.today(),
        )

    # =========================================================
    # HELPERS
    # =========================================================

    def create_provider(self):

        result = ProviderCreationWorkflow(
            request=ProviderCreationRequest(
                organization_id=self.organization.id,
                employee_id=self.employee.id,
                provider_number=(f"DOC-{uuid4().hex[:8].upper()}"),
                provider_type="physician",
                years_of_experience=5,
                bio="Workflow test provider",
                is_accepting_patients=True,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            result.success,
            result,
        )

        return Provider.objects.get(
            id=result.data.provider_id,
        )

    # =========================================================
    # TESTS
    # =========================================================

    def test_create_provider_workflow(self):

        provider = self.create_provider()

        self.assertEqual(
            provider.status,
            ProviderStatus.PENDING,
        )

    def test_verify_provider_workflow(self):

        provider = self.create_provider()

        provider.status = ProviderStatus.UNDER_REVIEW

        provider.save(
            update_fields=[
                "status",
            ],
        )

        result = ProviderVerificationWorkflow(
            request=ProviderVerificationRequest(
                provider_id=provider.id,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            result.success,
        )

        provider.refresh_from_db()

        self.assertEqual(
            provider.status,
            ProviderStatus.VERIFIED,
        )

    def test_activate_provider_workflow(self):

        provider = self.create_provider()

        provider.status = ProviderStatus.VERIFIED

        provider.save(
            update_fields=[
                "status",
            ],
        )

        result = ProviderActivationWorkflow(
            request=ProviderActivationRequest(
                provider_id=provider.id,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            result.success,
        )

        provider.refresh_from_db()

        self.assertEqual(
            provider.status,
            ProviderStatus.ACTIVE,
        )

    def test_assign_provider_workflow(self):

        provider = self.create_provider()

        provider.status = ProviderStatus.ACTIVE

        provider.save(
            update_fields=[
                "status",
            ],
        )

        department = Department.objects.create(
            organization=self.organization,
            name="Cardiology",
            code=f"CARD-{uuid4().hex[:6].upper()}",
        )

        result = ProviderAssignmentWorkflow(
            request=ProviderAssignmentRequest(
                provider_id=provider.id,
                organization_id=self.organization.id,
                department_id=department.id,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            result.success,
        )

    def test_update_provider_workflow(self):

        provider = self.create_provider()

        result = ProviderUpdateWorkflow(
            request=ProviderUpdateRequest(
                provider_id=provider.id,
                data={
                    "bio": "Updated workflow provider",
                    "years_of_experience": 10,
                },
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            result.success,
        )

        provider.refresh_from_db()

        self.assertEqual(
            provider.bio,
            "Updated workflow provider",
        )

        self.assertEqual(
            provider.years_of_experience,
            10,
        )

    def test_deactivate_provider_workflow(self):

        provider = self.create_provider()

        provider.status = ProviderStatus.ACTIVE

        provider.save(
            update_fields=[
                "status",
            ],
        )

        result = ProviderDeactivationWorkflow(
            request=ProviderDeactivationRequest(
                provider_id=provider.id,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            result.success,
        )

        provider.refresh_from_db()

        self.assertEqual(
            provider.status,
            ProviderStatus.INACTIVE,
        )
