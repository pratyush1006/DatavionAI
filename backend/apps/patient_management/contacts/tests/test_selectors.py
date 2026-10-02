"""
Tests for Contact selectors.
"""

from __future__ import annotations

from django.test import TestCase

from apps.patient_management.contacts.selectors import (
    get_contact_by_id,
)
from apps.patient_management.contacts.tests.factories import ContactFactory


class ContactSelectorTestCase(TestCase):
    """Tests for contact selectors."""

    def test_get_contact_by_id(self) -> None:
        contact = ContactFactory()

        result = get_contact_by_id(
            contact.pk,
        )

        self.assertEqual(
            result.pk,
            contact.pk,
        )
