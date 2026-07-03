"""
Tests for RBAC role selectors.
"""

from __future__ import annotations

from django.http import Http404

from apps.common.tests.base import BaseTestCase
from apps.rbac.selectors.permission import (
    get_permission_by_code,
    get_permission_by_id,
    get_permissions,
)
from apps.rbac.selectors.role import (
    get_role_by_code,
    get_role_by_id,
    get_roles,
)
from apps.rbac.selectors.role_permission import (
    get_permissions_for_role,
    get_role_permission_by_id,
    get_role_permissions,
    get_roles_for_permission,
)
from apps.rbac.selectors.user_role import (
    get_roles_for_user,
    get_user_role_by_id,
    get_user_roles,
    get_users_for_role,
)
from apps.rbac.tests.factories import (
    PermissionFactory,
    RoleFactory,
    RolePermissionFactory,
    UserFactory,
    UserRoleFactory,
)


class RoleSelectorTest(BaseTestCase):
    """
    Tests for role selectors.
    """

    def test_get_roles_returns_active_roles_only(self) -> None:
        """
        Only active roles should be returned by default.
        """
        active_role = RoleFactory(
            name="Administrator",
            is_active=True,
        )

        RoleFactory(
            name="Inactive Role",
            is_active=False,
        )

        roles = get_roles()

        self.assertEqual(
            roles.count(),
            1,
        )

        self.assertEqual(
            roles.first(),
            active_role,
        )

    def test_get_roles_include_inactive(self) -> None:
        """
        All roles should be returned when include_inactive=True.
        """
        RoleFactory(
            is_active=True,
        )

        RoleFactory(
            is_active=False,
        )

        roles = get_roles(
            include_inactive=True,
        )

        self.assertEqual(
            roles.count(),
            2,
        )

    def test_get_roles_are_ordered_by_name(self) -> None:
        """
        Roles should be ordered alphabetically.
        """
        RoleFactory(
            name="Zebra",
        )

        RoleFactory(
            name="Administrator",
        )

        roles = list(get_roles(include_inactive=True))

        self.assertEqual(
            roles[0].name,
            "Administrator",
        )

        self.assertEqual(
            roles[1].name,
            "Zebra",
        )

    def test_get_role_by_id(self) -> None:
        """
        A role should be retrieved by primary key.
        """
        role = RoleFactory()

        retrieved = get_role_by_id(
            role_id=role.id,
        )

        self.assertEqual(
            retrieved,
            role,
        )

    def test_get_role_by_id_not_found(self) -> None:
        """
        Unknown role ids should raise Http404.
        """
        with self.assertRaises(Http404):
            get_role_by_id(
                role_id=999999,
            )

    def test_get_role_by_code(self) -> None:
        """
        A role should be retrieved by code.
        """
        role = RoleFactory(
            code="ADMIN",
        )

        retrieved = get_role_by_code(
            code="ADMIN",
        )

        self.assertEqual(
            retrieved,
            role,
        )

    def test_get_role_by_code_not_found(self) -> None:
        """
        Unknown role codes should raise Http404.
        """
        with self.assertRaises(Http404):
            get_role_by_code(
                code="UNKNOWN",
            )


class PermissionSelectorsTestCase(BaseTestCase):
    """
    Tests for permission selectors.
    """

    def test_get_permissions_returns_active_permissions_only(self) -> None:
        """
        Only active permissions should be returned by default.
        """
        active_permission = PermissionFactory(
            name="Create User",
            is_active=True,
        )

        PermissionFactory(
            name="Inactive Permission",
            is_active=False,
        )

        permissions = get_permissions()

        self.assertEqual(
            permissions.count(),
            1,
        )

        self.assertEqual(
            permissions.first(),
            active_permission,
        )

    def test_get_permissions_include_inactive(self) -> None:
        """
        All permissions should be returned when include_inactive=True.
        """
        PermissionFactory(
            is_active=True,
        )

        PermissionFactory(
            is_active=False,
        )

        permissions = get_permissions(
            include_inactive=True,
        )

        self.assertEqual(
            permissions.count(),
            2,
        )

    def test_get_permissions_are_ordered_by_name(self) -> None:
        """
        Permissions should be ordered alphabetically.
        """
        PermissionFactory(
            name="Z Permission",
        )

        PermissionFactory(
            name="A Permission",
        )

        permissions = list(
            get_permissions(
                include_inactive=True,
            ),
        )

        self.assertEqual(
            permissions[0].name,
            "A Permission",
        )

        self.assertEqual(
            permissions[1].name,
            "Z Permission",
        )

    def test_get_permission_by_id(self) -> None:
        """
        A permission should be retrieved by primary key.
        """
        permission = PermissionFactory()

        retrieved = get_permission_by_id(
            permission_id=permission.id,
        )

        self.assertEqual(
            retrieved,
            permission,
        )

    def test_get_permission_by_id_not_found(self) -> None:
        """
        Unknown permission ids should raise Http404.
        """
        with self.assertRaises(Http404):
            get_permission_by_id(
                permission_id=999999,
            )

    def test_get_permission_by_code(self) -> None:
        """
        A permission should be retrieved by code.
        """
        permission = PermissionFactory(
            code="user.create",
        )

        retrieved = get_permission_by_code(
            code="user.create",
        )

        self.assertEqual(
            retrieved,
            permission,
        )

    def test_get_permission_by_code_not_found(self) -> None:
        """
        Unknown permission codes should raise Http404.
        """
        with self.assertRaises(Http404):
            get_permission_by_code(
                code="unknown.permission",
            )


class UserRoleSelectorsTestCase(BaseTestCase):
    """
    Tests for user role selectors.
    """

    def test_get_user_roles_returns_all_assignments(self) -> None:
        """
        All user-role assignments should be returned.
        """
        UserRoleFactory()
        UserRoleFactory()

        assignments = get_user_roles()

        self.assertEqual(
            assignments.count(),
            2,
        )

    def test_get_user_role_by_id(self) -> None:
        """
        A user-role assignment should be retrieved by id.
        """
        assignment = UserRoleFactory()

        retrieved = get_user_role_by_id(
            user_role_id=assignment.id,
        )

        self.assertEqual(
            retrieved,
            assignment,
        )

    def test_get_user_role_by_id_not_found(self) -> None:
        """
        Unknown ids should raise Http404.
        """
        with self.assertRaises(Http404):
            get_user_role_by_id(
                user_role_id=999999,
            )

    def test_get_roles_for_user(self) -> None:
        """
        Only assignments for the requested user should be returned.
        """
        user = UserFactory()

        assignment = UserRoleFactory(
            user=user,
        )

        UserRoleFactory()

        queryset = get_roles_for_user(
            user_id=user.id,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            assignment,
        )

    def test_get_users_for_role(self) -> None:
        """
        Only assignments for the requested role should be returned.
        """
        role = RoleFactory()

        assignment = UserRoleFactory(
            role=role,
        )

        UserRoleFactory()

        queryset = get_users_for_role(
            role_id=role.id,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            assignment,
        )


class RolePermissionSelectorsTestCase(BaseTestCase):
    """
    Tests for role permission selectors.
    """

    def test_get_role_permissions_returns_all_assignments(self) -> None:
        """
        All role-permission assignments should be returned.
        """
        RolePermissionFactory()
        RolePermissionFactory()

        assignments = get_role_permissions()

        self.assertEqual(
            assignments.count(),
            2,
        )

    def test_get_role_permission_by_id(self) -> None:
        """
        A role-permission assignment should be retrieved by id.
        """
        assignment = RolePermissionFactory()

        retrieved = get_role_permission_by_id(
            role_permission_id=assignment.id,
        )

        self.assertEqual(
            retrieved,
            assignment,
        )

    def test_get_role_permission_by_id_not_found(self) -> None:
        """
        Unknown ids should raise Http404.
        """
        with self.assertRaises(Http404):
            get_role_permission_by_id(
                role_permission_id=999999,
            )

    def test_get_permissions_for_role(self) -> None:
        """
        Only permissions assigned to the requested role should be returned.
        """
        role = RoleFactory()

        assignment = RolePermissionFactory(
            role=role,
        )

        RolePermissionFactory()

        queryset = get_permissions_for_role(
            role_id=role.id,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            assignment,
        )

    def test_get_roles_for_permission(self) -> None:
        """
        Only roles assigned to the requested permission should be returned.
        """
        permission = PermissionFactory()

        assignment = RolePermissionFactory(
            permission=permission,
        )

        RolePermissionFactory()

        queryset = get_roles_for_permission(
            permission_id=permission.id,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            assignment,
        )
