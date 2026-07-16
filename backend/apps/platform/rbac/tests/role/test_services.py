"""
Tests for Role services.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.rbac.services import (
    activate_role,
    create_role,
    deactivate_role,
    delete_role,
    make_default_role,
    update_role,
)
from apps.platform.rbac.tests.factories import (
    create_role as create_role_factory,
)


class RoleServiceTestCase(
    TestCase,
):
    """
    Tests for Role services.
    """

    def test_should_create_role(
        self,
    ) -> None:
        """
        create_role() should create a role.
        """

        validated_data = {
            "name": "Doctor",
        }

        role = create_role(
            validated_data=validated_data,
        )

        self.assertEqual(
            role.name,
            "Doctor",
        )

        self.assertIsNotNone(
            role.pk,
        )

    def test_should_update_role(
        self,
    ) -> None:
        """
        update_role() should update a role.
        """

        role = create_role_factory(
            name="Doctor",
        )

        updated = update_role(
            instance=role,
            validated_data={
                "name": "Senior Doctor",
            },
        )

        self.assertEqual(
            updated.name,
            "Senior Doctor",
        )

    def test_should_activate_role(
        self,
    ) -> None:
        """
        activate_role() should activate a role.
        """

        role = create_role_factory(
            is_active=False,
        )

        activate_role(
            instance=role,
        )

        role.refresh_from_db()

        self.assertTrue(
            role.is_active,
        )

    def test_should_deactivate_role(
        self,
    ) -> None:
        """
        deactivate_role() should deactivate a role.
        """

        role = create_role_factory()

        deactivate_role(
            instance=role,
        )

        role.refresh_from_db()

        self.assertFalse(
            role.is_active,
        )

    def test_should_make_default_role(
        self,
    ) -> None:
        """
        make_default_role() should mark a role as default.
        """

        role = create_role_factory(
            is_default=False,
        )

        make_default_role(
            instance=role,
        )

        role.refresh_from_db()

        self.assertTrue(
            role.is_default,
        )

    def test_should_delete_role(
        self,
    ) -> None:
        """
        delete_role() should soft delete a role.
        """

        role = create_role_factory()

        delete_role(
            instance=role,
        )

        self.assertFalse(
            role.__class__.objects.filter(
                pk=role.pk,
            ).exists(),
        )

        self.assertTrue(
            role.__class__.all_objects.filter(
                pk=role.pk,
            ).exists(),
        )

        role.refresh_from_db()

        self.assertTrue(
            role.is_deleted,
        )

        self.assertFalse(
            role.is_active,
        )


__all__ = [
    "RoleServiceTestCase",
]
