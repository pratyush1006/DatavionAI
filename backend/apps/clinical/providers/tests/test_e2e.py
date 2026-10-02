"""
Provider Lifecycle E2E Test.

DatavionOS Provider Lifecycle:

Tenant
    |
Organization
    |
RBAC
    |
Employee
    |
Provider Creation Workflow
    |
Verification Workflow
    |
Activation Workflow
    |
Assignment Workflow
    |
Update Workflow
    |
Deactivation Workflow
"""

from __future__ import annotations

import uuid
from datetime import date

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
from apps.common.middleware.context import (
    set_current_organization,
    set_current_tenant,
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


class ProviderLifecycleE2ETestCase(
    TestCase,
):
    """
    Complete provider lifecycle test.
    """

    # ============================================================
    # RBAC SEED
    # ============================================================

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

    # ============================================================
    # SETUP
    # ============================================================

    def setUp(self):

        self.tenant = Tenant.objects.create(
            name="Datavion Test Tenant",
            slug=f"tenant-{uuid.uuid4().hex[:8]}",
            tenant_type="ORGANIZATION",
            status="ACTIVE",
        )

        self.organization = Organization.objects.create(
            tenant=self.tenant,
            name="Datavion Healthcare Clinic",
            display_name="Datavion Healthcare Clinic",
            code=f"DVT-{uuid.uuid4().hex[:6].upper()}",
            slug=f"clinic-{uuid.uuid4().hex[:8]}",
            organization_type="CLINIC",
            status="ACTIVE",
            email="clinic@datavion.test",
        )

        self.user = User.objects.create_user(
            email="admin@datavion.test",
            password="Test@123456",
        )

        owner_role = self.seed_rbac()

        OrganizationRole.objects.create(
            organization=self.organization,
            user=self.user,
            role=owner_role,
            is_primary=True,
        )

        self.employee_user = User.objects.create_user(
            email=f"employee-{uuid.uuid4().hex[:8]}@test.com",
            password="Test@123456",
        )

        self.employee = Employee.objects.create(
            organization=self.organization,
            user=self.employee_user,
            employee_code=f"EMP-{uuid.uuid4().hex[:8].upper()}",
            designation="Physician",
            work_email=self.employee_user.email,
            phone_number="9999999999",
            employment_type="full_time",
            status="active",
            joining_date=date.today(),
        )

        self.department = Department.objects.create(
            organization=self.organization,
            name="Cardiology",
            code=f"CARD-{uuid.uuid4().hex[:4].upper()}",
        )

        set_current_tenant(
            self.tenant,
        )

        set_current_organization(
            self.organization,
        )

        self.context = WorkflowContext(
            actor_id=self.user.id,
            tenant_id=self.tenant.id,
        )

    # ============================================================
    # TEST
    # ============================================================

    def test_provider_full_lifecycle(self):

        #
        # CREATE
        #

        create_result = ProviderCreationWorkflow(
            request=ProviderCreationRequest(
                organization_id=self.organization.id,
                employee_id=self.employee.id,
                provider_number=f"DOC-{uuid.uuid4().hex[:8].upper()}",
                provider_type="physician",
                years_of_experience=5,
                bio="E2E Provider",
                is_accepting_patients=True,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            create_result.success,
            create_result,
        )

        provider = Provider.objects.get(
            id=create_result.data.provider_id,
        )

        self.assertEqual(
            provider.status,
            ProviderStatus.PENDING,
        )

        #
        # VERIFY
        #

        provider.status = ProviderStatus.UNDER_REVIEW

        provider.save(
            update_fields=[
                "status",
            ],
        )

        verify_result = ProviderVerificationWorkflow(
            request=ProviderVerificationRequest(
                provider_id=provider.id,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            verify_result.success,
            verify_result,
        )

        provider.refresh_from_db()

        self.assertEqual(
            provider.status,
            ProviderStatus.VERIFIED,
        )

        #
        # ACTIVATE
        #

        activate_result = ProviderActivationWorkflow(
            request=ProviderActivationRequest(
                provider_id=provider.id,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            activate_result.success,
            activate_result,
        )

        provider.refresh_from_db()

        self.assertEqual(
            provider.status,
            ProviderStatus.ACTIVE,
        )

        #
        # ASSIGN
        #

        assignment_result = ProviderAssignmentWorkflow(
            request=ProviderAssignmentRequest(
                provider_id=provider.id,
                organization_id=self.organization.id,
                department_id=self.department.id,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            assignment_result.success,
            assignment_result,
        )

        #
        # UPDATE
        #

        update_result = ProviderUpdateWorkflow(
            request=ProviderUpdateRequest(
                provider_id=provider.id,
                data={
                    "bio": "Updated Provider Profile",
                    "years_of_experience": 10,
                },
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            update_result.success,
            update_result,
        )

        provider.refresh_from_db()

        self.assertEqual(
            provider.bio,
            "Updated Provider Profile",
        )

        self.assertEqual(
            provider.years_of_experience,
            10,
        )

        #
        # DEACTIVATE
        #

        deactivate_result = ProviderDeactivationWorkflow(
            request=ProviderDeactivationRequest(
                provider_id=provider.id,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            deactivate_result.success,
            deactivate_result,
        )

        provider.refresh_from_db()

        self.assertEqual(
            provider.status,
            ProviderStatus.INACTIVE,
        )
