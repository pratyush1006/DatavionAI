"""
Model tests for Emergency Contacts.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)

from .factories import (
    EmergencyContactFactory,
)


class EmergencyContactModelTestCase(
    TestCase,
):
    """
    Tests for the EmergencyContact model.
    """

    def test_create_emergency_contact(self) -> None:
        """
        An emergency contact can be created.
        """

        contact = EmergencyContactFactory()

        self.assertIsInstance(
            contact,
            EmergencyContact,
        )

    def test_string_representation(self) -> None:
        """
        String representation should not be empty.
        """

        contact = EmergencyContactFactory()

        self.assertTrue(
            str(contact),
        )

    def test_full_name_property(self) -> None:
        """
        Full name property returns the complete name.
        """

        contact = EmergencyContactFactory(
            first_name="John",
            middle_name="A",
            last_name="Doe",
        )

        self.assertEqual(
            contact.full_name,
            "John A Doe",
        )

    def test_default_is_primary(self) -> None:
        """
        Default primary flag.
        """

        contact = EmergencyContactFactory()

        self.assertTrue(
            contact.is_primary,
        )

    def test_default_is_verified(self) -> None:
        """
        Contact is not verified initially.
        """

        contact = EmergencyContactFactory()

        self.assertFalse(
            contact.is_verified,
        )

    def test_soft_delete(self) -> None:
        """
        Soft delete marks the object as deleted.
        """

        contact = EmergencyContactFactory()

        contact.delete()

        contact.refresh_from_db()

        self.assertTrue(
            contact.is_deleted,
        )

        self.assertFalse(
            contact.is_active,
        )

    def test_restore(self) -> None:
        """
        Deleted contact can be restored.
        """

        contact = EmergencyContactFactory()

        contact.delete()

        contact.restore()

        contact.refresh_from_db()

        self.assertFalse(
            contact.is_deleted,
        )

        self.assertTrue(
            contact.is_active,
        )

    def test_hard_delete(self) -> None:
        """
        Hard delete permanently removes the record.
        """

        contact = EmergencyContactFactory()

        pk = contact.pk

        contact.hard_delete()

        self.assertFalse(
            EmergencyContact.all_objects.filter(
                pk=pk,
            ).exists(),
        )
