"""
Selector tests for Emergency Contacts.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.emergency_contacts.models import (
    EmergencyContact,
)
from apps.patient_management.emergency_contacts.selectors import (
    get_emergency_contact_by_id,
    get_primary_emergency_contact,
    list_emergency_contacts,
    list_organization_emergency_contacts,
    list_patient_emergency_contacts,
    search_emergency_contacts,
)

from .factories import (
    EmergencyContactFactory,
)


class EmergencyContactSelectorTestCase(
    TestCase,
):
    """
    Tests for Emergency Contact selectors.
    """

    def setUp(
        self,
    ) -> None:
        """
        Create test data.
        """

        self.contact = EmergencyContactFactory(
            first_name="John",
            last_name="Doe",
            is_primary=True,
        )

        self.organization = self.contact.organization

        self.patient = self.contact.patient

        EmergencyContactFactory(
            organization=self.organization,
            patient=self.patient,
            first_name="Jane",
            last_name="Smith",
            priority_order=2,
            is_primary=False,
        )

    def test_get_emergency_contact_by_id(
        self,
    ) -> None:
        """
        Retrieve emergency contact by id.
        """

        contact = get_emergency_contact_by_id(
            self.contact.id,
        )

        self.assertEqual(
            contact,
            self.contact,
        )

    def test_list_emergency_contacts(
        self,
    ) -> None:
        """
        List all emergency contacts.
        """

        queryset = list_emergency_contacts()

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_list_patient_emergency_contacts(
        self,
    ) -> None:
        """
        List contacts for a patient.
        """

        queryset = list_patient_emergency_contacts(
            patient=self.patient,
        )

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_list_organization_emergency_contacts(
        self,
    ) -> None:
        """
        List contacts for an organization.
        """

        queryset = list_organization_emergency_contacts(
            organization=self.organization,
        )

        self.assertEqual(
            queryset.count(),
            2,
        )

    def test_get_primary_emergency_contact(
        self,
    ) -> None:
        """
        Retrieve the primary emergency contact.
        """

        contact = get_primary_emergency_contact(
            patient=self.patient,
        )

        self.assertEqual(
            contact,
            self.contact,
        )

    def test_search_emergency_contacts(
        self,
    ) -> None:
        """
        Search emergency contacts.
        """

        queryset = search_emergency_contacts(
            search="John",
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            self.contact,
        )

    def test_soft_deleted_contact_not_returned(
        self,
    ) -> None:
        """
        Soft deleted contacts should not appear.
        """

        self.contact.delete()

        queryset = list_emergency_contacts()

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_selector_returns_queryset(
        self,
    ) -> None:
        """
        Selector returns a queryset.
        """

        queryset = list_emergency_contacts()

        self.assertIsInstance(
            queryset,
            type(EmergencyContact.objects.all()),
        )
