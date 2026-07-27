"""
Tests for Contact models.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.contacts.tests.factories import ContactFactory


class ContactModelTestCase(TestCase):
    """Tests for Contact."""

    def test_create_contact(self) -> None:
        contact = ContactFactory()

        self.assertIsNotNone(contact.pk)

    def test_string_representation(self) -> None:
        contact = ContactFactory()

        self.assertEqual(
            str(contact),
            contact.value,
        )
