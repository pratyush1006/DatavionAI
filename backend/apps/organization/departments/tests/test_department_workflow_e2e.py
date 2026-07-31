"""
Department workflow end-to-end tests.

Validates complete lifecycle:

Tenant
    |
Organization
    |
RBAC
    |
Department Creation
    |
Department Update
    |
Department Archive
"""

from __future__ import annotations

from django.test import TransactionTestCase

from apps.core.workflows import (
    WorkflowContext,
)
from apps.organization.departments.models import (
    Department,
)
from apps.organization.departments.workflows import (
    DepartmentCreationRequest,
    DepartmentCreationWorkflow,
    DepartmentDeletionRequest,
    DepartmentDeletionWorkflow,
    DepartmentUpdateRequest,
    DepartmentUpdateWorkflow,
)
from apps.platform.accounts.models import (
    User,
)
from apps.platform.organizations.models import (
    Organization,
)
from apps.platform.rbac.engines import (
    user_has_permission,
)
from apps.platform.rbac.models import (
    OrganizationRole,
    Permission,
    Role,
    RolePermission,
)
from apps.platform.tenancy.models import (
    Tenant,
)


class DepartmentWorkflowE2ETestCase(
    TransactionTestCase,
):
    """
    Full department lifecycle test.
    """

    reset_sequences = True

    def setUp(
        self,
    ):
        """
        Prepare tenant, organization,
        user and RBAC.
        """

        self.user = User.objects.create_user(
            email="department.e2e@datavion.ai",
            password="Test@12345",
        )

        self.tenant = Tenant.objects.create(
            name="Department E2E Tenant",
            slug="department-e2e",
        )

        self.organization = Organization.objects.create(
            tenant=self.tenant,
            name="Department E2E Hospital",
            code="DEPT-E2E",
        )

        #
        # Create Role
        #

        self.role = Role.objects.create(
            name="Organization Administrator E2E",
            code="organization_administrator_e2e",
            description=("Organization administrator test role."),
            is_system=False,
        )

        OrganizationRole.objects.create(
            organization=self.organization,
            user=self.user,
            role=self.role,
        )

        #
        # Create Permissions
        #

        for permission_code, action in (
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
        ):
            permission = Permission.objects.filter(
                code=permission_code,
            ).first()

            if permission is None:
                permission = Permission.objects.create(
                    code=permission_code,
                    name=(
                        permission_code.replace(
                            ".",
                            " ",
                        ).title()
                    ),
                    description=(f"{permission_code} permission"),
                    module="departments",
                    action=action,
                    scope="organization",
                )

            RolePermission.objects.get_or_create(
                role=self.role,
                permission=permission,
            )

        self.context = WorkflowContext(
            actor_id=self.user.id,
            tenant_id=self.tenant.id,
        )

    def test_department_complete_lifecycle(
        self,
    ):
        """
        Test:

        Create
        Update
        Archive
        """

        #
        # Permission validation
        #

        self.assertTrue(
            user_has_permission(
                user=self.user,
                permission="departments.create",
                organization=self.organization,
            )
        )

        self.assertTrue(
            user_has_permission(
                user=self.user,
                permission="departments.update",
                organization=self.organization,
            )
        )

        self.assertTrue(
            user_has_permission(
                user=self.user,
                permission="departments.delete",
                organization=self.organization,
            )
        )

        #
        # CREATE
        #

        create_result = DepartmentCreationWorkflow(
            request=DepartmentCreationRequest(
                organization_id=self.organization.id,
                name="Cardiology E2E",
                code="CARD-E2E",
                description=("Workflow test department"),
                department_type="CLINICAL",
                phone="9999999999",
                email=("cardiology@test.com"),
                location="Block A",
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            create_result.success,
        )

        department = Department.all_objects.get(
            code="CARD-E2E",
        )

        self.assertEqual(
            department.name,
            "Cardiology E2E",
        )

        #
        # UPDATE
        #

        update_result = DepartmentUpdateWorkflow(
            request=DepartmentUpdateRequest(
                department_id=department.id,
                data={
                    "name": ("Cardiology Advanced Center"),
                },
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            update_result.success,
        )

        department.refresh_from_db()

        self.assertEqual(
            department.name,
            "Cardiology Advanced Center",
        )

        #
        # DELETE / ARCHIVE
        #

        delete_result = DepartmentDeletionWorkflow(
            request=DepartmentDeletionRequest(
                department_id=department.id,
            ),
        ).execute(
            context=self.context,
        )

        self.assertTrue(
            delete_result.success,
        )

        department.refresh_from_db()

        #
        # Soft delete verification
        #

        self.assertTrue(
            department.is_deleted,
        )

        self.assertIsNotNone(
            department.deleted_at,
        )

        #
        # Default manager hides deleted data
        #

        self.assertFalse(
            Department.objects.filter(
                code="CARD-E2E",
            ).exists()
        )

        #
        # All objects returns archived data
        #

        self.assertTrue(
            Department.all_objects.filter(
                code="CARD-E2E",
            ).exists()
        )
