"""
Service tests for Emergency Contacts.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.emergency_contacts.services import (
    EmergencyContactService,
)

from .factories import (
    EmergencyContactFactory,
)


class EmergencyContactServiceTestCase(
    TestCase,
):
    """
    Tests for EmergencyContactService.
    """

    def setUp(
        self,
    ) -> None:
        """
        Create test data.
        """

        self.contact = EmergencyContactFactory()

        self.organization = self.contact.organization

        self.patient = self.contact.patient

    def test_update_emergency_contact(
        self,
    ) -> None:
        """
        Emergency contact can be updated.
        """

        updated = EmergencyContactService.update(
            emergency_contact=self.contact,
            data={
                "first_name": "Jane",
            },
        )

        self.assertEqual(
            updated.first_name,
            "Jane",
        )

    def test_verify_contact(
        self,
    ) -> None:
        """
        Contact can be verified.
        """

        EmergencyContactService.verify(
            emergency_contact=self.contact,
            verified_by=None,
        )

        self.contact.refresh_from_db()

        self.assertTrue(
            self.contact.is_verified,
        )

        self.assertIsNotNone(
            self.contact.verified_at,
        )

    def test_delete_contact(
        self,
    ) -> None:
        """
        Contact is soft deleted.
        """

        EmergencyContactService.delete(
            emergency_contact=self.contact,
        )

        self.contact.refresh_from_db()

        self.assertTrue(
            self.contact.is_deleted,
        )

    def test_primary_contact_replaced(
        self,
    ) -> None:
        """
        Creating a new primary contact demotes
        the previous primary contact.
        """

        first = EmergencyContactFactory(
            patient=self.patient,
            organization=self.organization,
            is_primary=True,
            priority_order=1,
        )

        second = EmergencyContactService.create(
            organization=self.organization,
            patient=self.patient,
            data={
                "first_name": "Mary",
                "last_name": "Doe",
                "relationship": first.relationship,
                "mobile_number": "9999999999",
                "priority_order": 2,
                "is_primary": True,
            },
        )

        first.refresh_from_db()

        self.assertFalse(
            first.is_primary,
        )

        self.assertTrue(
            second.is_primary,
        )

    def test_update_primary_contact(
        self,
    ) -> None:
        """
        Updating a contact to primary demotes
        the existing primary contact.
        """

        second = EmergencyContactFactory(
            patient=self.patient,
            organization=self.organization,
            is_primary=False,
            priority_order=2,
        )

        EmergencyContactService.update(
            emergency_contact=second,
            data={
                "is_primary": True,
            },
        )

        self.contact.refresh_from_db()
        second.refresh_from_db()

        self.assertFalse(
            self.contact.is_primary,
        )

        self.assertTrue(
            second.is_primary,
        )

    def test_restore_contact(
        self,
    ) -> None:
        """
        Deleted contact can be restored.
        """

        self.contact.delete()

        self.contact.restore()

        self.contact.refresh_from_db()

        self.assertFalse(
            self.contact.is_deleted,
        )

    def test_service_returns_model(
        self,
    ) -> None:
        """
        Update returns the updated model instance.
        """

        result = EmergencyContactService.update(
            emergency_contact=self.contact,
            data={},
        )

        self.assertEqual(
            result,
            self.contact,
        )
