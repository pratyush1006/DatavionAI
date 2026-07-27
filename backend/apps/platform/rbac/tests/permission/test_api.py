"""
Tests for Permission API.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.platform.organizations.tests.factories import (
    OrganizationFactory,
)
from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
)
from apps.platform.rbac.engines import (
    user_has_permission,
)
from apps.platform.rbac.models import (
    Role,
)
from apps.platform.rbac.tests.factories.organization_role import (
    OrganizationRoleFactory,
)
from apps.platform.rbac.tests.factories.permission import (
    create_permission,
)
from apps.platform.rbac.tests.factories.role_permission import (
    RolePermissionFactory,
)

User = get_user_model()


class PermissionAPITestCase(
    APITestCase,
):
    """
    Tests for Permission API.
    """

    def setUp(
        self,
    ) -> None:
        """
        Setup RBAC authenticated user.
        """

        self.user = User.objects.create_user(
            email="admin@datavion.ai",
            password="Password@123",
        )

        self.organization = OrganizationFactory()

        self.role = Role.objects.create(
            name="Organization Owner",
            code="organization_owner",
            is_system=True,
            is_active=True,
            is_assignable=True,
            is_editable=False,
            is_deletable=False,
        )

        OrganizationRoleFactory(
            organization=self.organization,
            user=self.user,
            role=self.role,
            is_primary=True,
        )

        #
        # Grant full permission lifecycle
        #
        # Required by:
        #
        # CanViewPermission
        # CanCreatePermission
        # CanUpdatePermission
        # CanDeletePermission
        #
        for action in (
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.DELETE,
        ):
            permission = create_permission(
                module=PermissionModule.RBAC,
                action=action,
                scope=PermissionScope.ORGANIZATION,
            )

            RolePermissionFactory(
                role=self.role,
                permission=permission,
            )

        #
        # Verify RBAC setup
        #
        assert (
            user_has_permission(
                user=self.user,
                permission="rbac.create",
                organization=self.organization,
            )
            is True
        )

        assert (
            user_has_permission(
                user=self.user,
                permission="rbac.delete",
                organization=self.organization,
            )
            is True
        )

        self.client.force_authenticate(
            user=self.user,
        )

        self.list_url = reverse(
            "rbac-api:permissions:permission-list",
        )

    def get_organization_headers(
        self,
    ) -> dict:
        """
        Return organization context headers.
        """

        return {
            "HTTP_X_ORGANIZATION_ID": str(
                self.organization.id,
            ),
        }

    def test_list_permissions(
        self,
    ) -> None:
        """
        List permissions.
        """

        create_permission()

        response = self.client.get(
            self.list_url,
            **self.get_organization_headers(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_permission(
        self,
    ) -> None:
        """
        Create permission.
        """

        response = self.client.post(
            self.list_url,
            {
                "module": PermissionModule.PATIENTS,
                "action": PermissionAction.VIEW,
                "scope": PermissionScope.ORGANIZATION,
            },
            format="json",
            **self.get_organization_headers(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_detail_permission(
        self,
    ) -> None:
        """
        Retrieve permission.
        """

        permission = create_permission()

        url = reverse(
            "rbac-api:permissions:permission-detail",
            kwargs={
                "permission_id": permission.id,
            },
        )

        response = self.client.get(
            url,
            **self.get_organization_headers(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_permission(
        self,
    ) -> None:
        """
        Update permission.
        """

        permission = create_permission()

        url = reverse(
            "rbac-api:permissions:permission-detail",
            kwargs={
                "permission_id": permission.id,
            },
        )

        response = self.client.patch(
            url,
            {
                "action": PermissionAction.UPDATE,
            },
            format="json",
            **self.get_organization_headers(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_permission(
        self,
    ) -> None:
        """
        Delete permission.
        """

        permission = create_permission()

        url = reverse(
            "rbac-api:permissions:permission-detail",
            kwargs={
                "permission_id": permission.id,
            },
        )

        response = self.client.delete(
            url,
            **self.get_organization_headers(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )


__all__ = [
    "PermissionAPITestCase",
]
